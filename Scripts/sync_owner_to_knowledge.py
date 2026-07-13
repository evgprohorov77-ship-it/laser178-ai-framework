#!/usr/bin/env python3
"""
Синхронизация Owner Portal → Knowledge.

Поддерживает два режима:
1. Legacy: читает YAML из Owner/.
2. Master profile: читает Owner/MASTER_PROFILE.yaml и генерирует 5 YAML в Owner/.

Использование:
    python3 Scripts/sync_owner_to_knowledge.py [--master]
    python3 Scripts/sync_owner_to_knowledge.py --dry-run
"""

import argparse
import re
import shutil
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent
OWNER_DIR = ROOT / "Owner"
KNOWLEDGE_DIR = ROOT / "Knowledge" / "Company"


def load_yaml(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_yaml(path: Path, data: dict, comment: str = ""):
    content = yaml.dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False)
    if comment:
        content = f"# {comment}\n{content}"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def clean_nulls(data):
    """Удаляем None значения на верхнем уровне словарей/списков для чистоты."""
    if isinstance(data, dict):
        return {k: clean_nulls(v) for k, v in data.items() if v is not None}
    if isinstance(data, list):
        return [clean_nulls(item) for item in data]
    return data


def build_company_profile(master: dict) -> dict:
    company = master.get("company", {})
    data = {
        "id": "company_profile",
        "version": master.get("version", "1.0.0"),
        "owner_portal": True,
        "source": "owner_edited",
        "entity_type": "company",
        "status": "active",
        "verification": "pending",
        "company": {
            "legal_name": wrap(company.get("legal_name"), "conversation"),
            "brand_name": wrap(company.get("brand_name"), "conversation"),
            "website": wrap(company.get("website"), "conversation"),
            "established_year": wrap(company.get("established_year"), "conversation", verified=False),
            "value_proposition": wrap(company.get("value_proposition"), "owner_edited", verified=False),
            "mission": wrap(company.get("mission"), "owner_edited", verified=False),
            "city_for_seo": wrap(company.get("city_for_seo"), "conversation"),
            "region": wrap(company.get("region"), "conversation"),
            "country": wrap(company.get("country"), "conversation"),
        }
    }
    return clean_nulls(data)


def build_contacts(master: dict) -> dict:
    contacts = master.get("contacts", {})
    messengers = contacts.get("messengers", {})
    social = contacts.get("social", {})
    data = {
        "id": "contacts",
        "version": master.get("version", "1.0.0"),
        "owner_portal": True,
        "source": "owner_edited",
        "entity_type": "contact_card",
        "status": "active",
        "verification": "pending",
        "contacts": {
            "website": wrap(master.get("company", {}).get("website"), "conversation"),
            "address": wrap(contacts.get("address"), "conversation"),
            "arrival": wrap(contacts.get("arrival"), "conversation"),
            "phone": wrap(contacts.get("phone"), "conversation"),
            "phone_alt": wrap(contacts.get("phone_alt"), "conversation", verified=False),
            "email": wrap(contacts.get("email"), "conversation"),
            "business_hours": wrap(contacts.get("business_hours"), "conversation"),
            "by_appointment": wrap(contacts.get("by_appointment", True), "conversation"),
            "messengers": {
                "whatsapp": wrap(messengers.get("whatsapp"), "conversation"),
                "telegram": wrap(messengers.get("telegram"), "conversation"),
                "viber": wrap(messengers.get("viber"), "conversation", verified=False),
            },
            "social": {
                "vk": wrap(social.get("vk"), "conversation", verified=False),
                "instagram": wrap(social.get("instagram"), "conversation", verified=False),
                "youtube": wrap(social.get("youtube"), "conversation", verified=False),
            },
            "map_link": wrap(contacts.get("map_link"), "conversation", verified=False),
            "yandex_maps": wrap(contacts.get("yandex_maps"), "conversation", verified=False),
            "google_maps": wrap(contacts.get("google_maps"), "conversation", verified=False),
        }
    }
    return clean_nulls(data)


def build_services(master: dict) -> dict:
    services = master.get("services", [])
    services_out = []
    for svc in services:
        services_out.append(clean_nulls({
            "id": svc["id"],
            "name": wrap(svc["name"], "owner_edited"),
            "short_description": wrap(svc.get("short_description", ""), "owner_edited", verified=False),
            "unit": wrap(svc.get("unit", ""), "owner_edited"),
            "public": wrap(svc.get("public", False), "owner_edited"),
        }))
    return {
        "id": "services",
        "version": master.get("version", "1.0.0"),
        "owner_portal": True,
        "source": "owner_edited",
        "entity_type": "service_catalog",
        "status": "active",
        "verification": "pending",
        "services": services_out,
    }


def build_guarantees(master: dict) -> dict:
    guarantees = master.get("guarantees", [])
    out = []
    for g in guarantees:
        out.append(clean_nulls({
            "type": g["type"],
            "title": wrap(g["title"], "owner_edited"),
            "duration": wrap(g.get("duration"), "owner_edited", verified=False),
            "description": wrap(g.get("description", ""), "owner_edited", verified=False),
            "verified": wrap(g.get("verified", False), "owner_edited", verified=False),
        }))
    return {
        "id": "guarantees",
        "version": master.get("version", "1.0.0"),
        "owner_portal": True,
        "source": "owner_edited",
        "entity_type": "guarantee_policy",
        "status": "active",
        "verification": "pending",
        "guarantees": out,
    }


def build_pricing(master: dict) -> dict:
    policy = master.get("pricing_policy", {})
    price_groups = master.get("price_groups", [])
    packages = master.get("packages", [])

    price_items = []
    for group in price_groups:
        for item in group.get("items", []):
            price_items.append(clean_nulls({
                "id": item["id"],
                "name": wrap(item["name"], "owner_edited"),
                "group": group["id"],
                "unit": wrap(item.get("unit", ""), "owner_edited"),
                "base_price": wrap(item.get("base_price"), "owner_edited", verified=False),
                "public": wrap(item.get("public", False), "owner_edited"),
            }))

    packages_out = []
    for pkg in packages:
        packages_out.append(clean_nulls({
            "id": pkg["id"],
            "name": wrap(pkg["name"], "owner_edited"),
            "description": wrap(pkg.get("description", ""), "owner_edited", verified=False),
            "public": wrap(pkg.get("public", False), "owner_edited"),
        }))

    return {
        "id": "prices",
        "version": master.get("version", "1.0.0"),
        "owner_portal": True,
        "source": "owner_edited",
        "entity_type": "price_catalog",
        "status": "active",
        "verification": "pending",
        "pricing_policy": {
            "material_markup_percent": wrap(policy.get("material_markup_percent", 5), "owner_edited"),
            "rounding_step": wrap(policy.get("rounding_step", 50), "owner_edited"),
            "currency": wrap(policy.get("currency", "RUB"), "owner_edited"),
        },
        "price_groups": [{"id": g["id"], "name": wrap(g["name"], "owner_edited")} for g in price_groups],
        "price_items": price_items,
        "packages": packages_out,
    }


def wrap(value, source, verified=True):
    """Обернуть значение в стандартный Knowledge-формат."""
    if isinstance(value, bool):
        return {"value": value, "source": source, "verified": verified}
    if value is None:
        return {"value": None, "source": source, "verified": False}
    return {"value": value, "source": source, "verified": verified}


def sync_to_knowledge(owner_file: str, knowledge_file: str, dry_run: bool):
    owner_path = OWNER_DIR / owner_file
    knowledge_path = KNOWLEDGE_DIR / knowledge_file
    if not owner_path.exists():
        raise FileNotFoundError(f"Owner file not found: {owner_path}")
    data = load_yaml(owner_path)
    if dry_run:
        print(f"[DRY-RUN] Would write {knowledge_path}")
        return
    save_yaml(knowledge_path, data, f"Generated from {owner_file}")
    print(f"[SYNC] {owner_path} -> {knowledge_path}")


def generate_owner_files_from_master(dry_run: bool):
    master = load_yaml(OWNER_DIR / "MASTER_PROFILE.yaml")
    mappings = [
        ("company_profile.yaml", build_company_profile(master)),
        ("contacts.yaml", build_contacts(master)),
        ("services.yaml", build_services(master)),
        ("guarantees.yaml", build_guarantees(master)),
        ("pricing.yaml", build_pricing(master)),
    ]
    for filename, data in mappings:
        path = OWNER_DIR / filename
        if dry_run:
            print(f"[DRY-RUN] Would write {path}")
        else:
            save_yaml(path, data, f"Auto-generated from MASTER_PROFILE.yaml — edit only MASTER_PROFILE.yaml")
            print(f"[GENERATED] {path}")


def main():
    parser = argparse.ArgumentParser(description="Sync Owner Portal to Knowledge")
    parser.add_argument("--dry-run", action="store_true", help="Do not write files")
    parser.add_argument("--master", action="store_true", default=True, help="Use MASTER_PROFILE.yaml (default)")
    parser.add_argument("--legacy", action="store_true", help="Use individual Owner YAML files")
    args = parser.parse_args()

    if args.legacy:
        # Legacy mode: individual Owner files
        sync_to_knowledge("company_profile.yaml", "company.yaml", args.dry_run)
        sync_to_knowledge("contacts.yaml", "contacts.yaml", args.dry_run)
        sync_to_knowledge("services.yaml", "services.yaml", args.dry_run)
        sync_to_knowledge("guarantees.yaml", "guarantees.yaml", args.dry_run)
        sync_to_knowledge("pricing.yaml", "prices.yaml", args.dry_run)
    else:
        # Master profile mode
        generate_owner_files_from_master(args.dry_run)
        if not args.dry_run:
            sync_to_knowledge("company_profile.yaml", "company.yaml", False)
            sync_to_knowledge("contacts.yaml", "contacts.yaml", False)
            sync_to_knowledge("services.yaml", "services.yaml", False)
            sync_to_knowledge("guarantees.yaml", "guarantees.yaml", False)
            sync_to_knowledge("pricing.yaml", "prices.yaml", False)

    print("[DONE]")


if __name__ == "__main__":
    main()
