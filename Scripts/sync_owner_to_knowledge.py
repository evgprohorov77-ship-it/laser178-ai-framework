#!/usr/bin/env python3
"""
Синхронизация Owner Portal → Knowledge.

Что делает:
1. Читает YAML из Owner/.
2. Преобразует формат owner_portal в формат Knowledge (value/verified/source/public).
3. Обновляет соответствующие файлы в Knowledge/Company/.
4. Запускает validate_knowledge.py.
5. Показывает diff для review.

Использование:
    python3 Scripts/sync_owner_to_knowledge.py [--dry-run]
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent
OWNER_DIR = ROOT / "Owner"
KNOWLEDGE_DIR = ROOT / "Knowledge" / "Company"

OWNER_TO_KNOWLEDGE = {
    "company_profile.yaml": "company.yaml",
    "contacts.yaml": "contacts.yaml",
    "services.yaml": "services.yaml",
    "guarantees.yaml": "guarantees.yaml",
    "pricing.yaml": ["prices.yaml", "materials.yaml"],
}


def normalize_value(owner_value, public_default=True):
    """Преобразует структуру Owner Portal в Knowledge."""
    if isinstance(owner_value, dict) and "value" in owner_value:
        public = owner_value.get("public", public_default)
        return {
            "value": owner_value["value"],
            "verified": True,
            "source": "owner_edited",
            "public": public,
        }
    if isinstance(owner_value, list):
        return [normalize_value(item, public_default) for item in owner_value]
    if isinstance(owner_value, dict):
        return {k: normalize_value(v, public_default) for k, v in owner_value.items()}
    return {"value": owner_value, "verified": True, "source": "owner_edited", "public": public_default}


def load_yaml(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_yaml(path: Path, data):
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)


def sync_file(owner_file: Path, knowledge_target: str, dry_run: bool):
    owner_data = load_yaml(owner_file)
    # Remove owner_portal metadata from synced knowledge
    owner_data.pop("owner_portal", None)
    owner_data.pop("source", None)

    normalized = normalize_value(owner_data)
    # Keep top-level id/version/entity_type/status/verification from original Knowledge if exists
    knowledge_path = KNOWLEDGE_DIR / knowledge_target
    if knowledge_path.exists():
        existing = load_yaml(knowledge_path)
        # Preserve fields that Owner should not override
        for key in ["id", "version", "entity_type", "status", "verification"]:
            if key in existing:
                normalized[key] = existing[key]

    if dry_run:
        print(f"[DRY-RUN] Would write {knowledge_path}")
        return

    save_yaml(knowledge_path, normalized)
    print(f"[SYNC] {owner_file.name} → {knowledge_target}")


def sync_pricing(owner_file: Path, dry_run: bool):
    data = load_yaml(owner_file)
    data.pop("owner_portal", None)
    data.pop("source", None)

    # Sync prices.yaml
    prices_path = KNOWLEDGE_DIR / "prices.yaml"
    prices = {
        "id": "prices",
        "version": "1.0.0",
        "entity_type": "price_catalog",
        "status": "draft",
        "verification": "pending",
    }

    pricing_policy = data.get("pricing_policy", {})
    prices["pricing_model"] = {
        "value": "Класс кузова → марка → модель. Арматурные работы — единица 'снятие+установка'. Материалы с наценкой 5% и округлением до 50 ₽.",
        "verified": True,
        "source": "owner_edited",
    }
    prices["markup_percent"] = normalize_value(pricing_policy.get("markup_percent", 5))
    prices["rounding"] = normalize_value(pricing_policy.get("rounding", 50))
    prices["client_facing_text"] = normalize_value(pricing_policy.get("client_facing_text", "без формулировок 'от'"))

    # Laser cleaning
    laser = data.get("laser_cleaning_rates", [])
    prices["laser_cleaning_rates"] = [
        {
            "name": normalize_value(item["name"]),
            "rate_per_m2": normalize_value(item["rate_per_m2"]),
            "note": normalize_value("Базовая ставка без мультипликаторов."),
        }
        for item in laser
    ]

    # Surface preparation
    prices["surface_preparation_base"] = normalize_value(data.get("surface_preparation", {}).get("base_price", 4000))

    # Anticor labor
    labor = data.get("anticor_labor_by_body", {})
    prices["anticor_labor_by_body"] = {
        k: normalize_value(v)
        for k, v in labor.items()
        if k != "public"
    }

    # Additional coatings
    coatings = data.get("additional_coatings", {})
    prices["additional_coatings"] = {
        "zinc_primer_per_m2": normalize_value(coatings.get("zinc_primer_per_m2", 1000)),
        "epoxy_primer_per_m2": normalize_value(coatings.get("epoxy_primer_per_m2", 500)),
    }

    # Package multipliers
    multipliers = data.get("package_multipliers", {})
    prices["package_multipliers"] = {
        k: normalize_value(v)
        for k, v in multipliers.items()
        if k != "public"
    }

    prices["notes"] = [
        normalize_value("Цены и коэффициенты подтверждены владельцем через Owner Portal."),
        normalize_value("public: false в Owner Portal означает, что цена не публикуется напрямую."),
    ]

    # Sync materials.yaml
    materials_path = KNOWLEDGE_DIR / "materials.yaml"
    materials = {
        "id": "materials",
        "version": "1.0.0",
        "entity_type": "material_catalog",
        "status": "draft",
        "verification": "pending",
    }
    materials["pricing_policy"] = {
        "markup_percent": normalize_value(pricing_policy.get("markup_percent", 5)),
        "rounding": normalize_value(pricing_policy.get("rounding", 50)),
        "client_facing_text": normalize_value(pricing_policy.get("client_facing_text", "без формулировок 'от'")),
        "verified": True,
        "source": "owner_edited",
    }
    materials["materials"] = [
        {
            "name": normalize_value(item["name"]),
            "purchase_price_per_liter": normalize_value(item.get("purchase_price_per_liter")),
            "public": item.get("public", False),
        }
        for item in data.get("materials", [])
    ]
    materials["suppliers"] = [
        normalize_value("Dinitrol"),
        normalize_value("ONB Master"),
        normalize_value("MasterWAX"),
    ]
    materials["notes"] = [
        normalize_value("Материалы и цены подтверждены владельцем через Owner Portal."),
        normalize_value("public: false в Owner Portal означает, что цена не публикуется напрямую."),
    ]

    if dry_run:
        print(f"[DRY-RUN] Would write {prices_path} and {materials_path}")
        return

    save_yaml(prices_path, prices)
    save_yaml(materials_path, materials)
    print(f"[SYNC] {owner_file.name} → prices.yaml + materials.yaml")


def main():
    parser = argparse.ArgumentParser(description="Sync Owner Portal to Knowledge")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be changed")
    args = parser.parse_args()

    if not OWNER_DIR.exists():
        print(f"[ERROR] Owner directory not found: {OWNER_DIR}")
        sys.exit(1)

    for owner_name, target in OWNER_TO_KNOWLEDGE.items():
        owner_file = OWNER_DIR / owner_name
        if not owner_file.exists():
            print(f"[SKIP] {owner_name} not found")
            continue

        if owner_name == "pricing.yaml":
            sync_pricing(owner_file, args.dry_run)
        else:
            sync_file(owner_file, target, args.dry_run)

    print("\n[SYNC] Running validate_knowledge.py...")
    if args.dry_run:
        print("[DRY-RUN] Skipping validation")
        return

    result = subprocess.run(
        [sys.executable, str(ROOT / "Scripts" / "validate_knowledge.py")],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
