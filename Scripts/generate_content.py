#!/usr/bin/env python3
"""
Генератор контента из Knowledge.

Создаёт черновики страниц и статей на основе verified Knowledge.
Использование:
    python3 Scripts/generate_content.py

Пока что поддерживает ручной ввод template/params. В будущем может быть расширен.
"""

import argparse
import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = ROOT / "Knowledge" / "Company"
CONTENT_DIR = ROOT / "Content"
DRAFTS_DIR = CONTENT_DIR / "Drafts"
FRAGMENTS_DIR = CONTENT_DIR / "Fragments"


def load_yaml(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_fragment(name: str) -> str:
    path = FRAGMENTS_DIR / f"{name}.md"
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""


def get_value(data, *keys, default=""):
    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return default
    if isinstance(data, dict):
        return data.get("value", default)
    return data


def resolve_placeholders(text: str, context: dict) -> str:
    def repl(match):
        key = match.group(1).strip()
        return str(context.get(key, f"[needs verification:{key}]"))
    return re.sub(r"\{\{\s*(.+?)\s*\}\}", repl, text)


def build_context():
    company = load_yaml(KNOWLEDGE_DIR / "company.yaml")
    contacts = load_yaml(KNOWLEDGE_DIR / "contacts.yaml")
    services = load_yaml(KNOWLEDGE_DIR / "services.yaml")
    guarantees = load_yaml(KNOWLEDGE_DIR / "guarantees.yaml")
    prices = load_yaml(KNOWLEDGE_DIR / "prices.yaml")

    ctx = {}
    ctx["company.brand_name"] = get_value(company, "company", "brand_name")
    ctx["company.city_for_seo"] = get_value(company, "company", "city_for_seo")
    ctx["company.region"] = get_value(company, "company", "region")
    ctx["company.mission"] = get_value(company, "mission")
    ctx["contacts.address"] = get_value(contacts, "contacts", "address")
    ctx["contacts.arrival"] = get_value(contacts, "contacts", "arrival")
    ctx["contacts.phone"] = get_value(contacts, "contacts", "phone")
    ctx["contacts.email"] = get_value(contacts, "contacts", "email")
    ctx["contacts.business_hours"] = get_value(contacts, "contacts", "business_hours")
    ctx["cta_fragment"] = load_fragment("cta")
    ctx["contacts_fragment"] = load_fragment("contacts_block")
    ctx["guarantee_notice"] = load_fragment("guarantee_notice")

    # Services
    for svc in services.get("services", []):
        sid = svc.get("id")
        ctx[f"service.{sid}.name"] = get_value(svc, "name")
        ctx[f"service.{sid}.description"] = get_value(svc, "short_description")
        ctx[f"service.{sid}.unit"] = get_value(svc, "unit")

    # Guarantees
    for g in guarantees.get("guarantees", []):
        gtype = g.get("type")
        ctx[f"guarantee.{gtype}.title"] = get_value(g, "title")
        ctx[f"guarantee.{gtype}.duration"] = get_value(g, "duration")

    return ctx


def generate_page_service(service_id: str, ctx: dict) -> str:
    name = ctx.get(f"service.{service_id}.name", service_id)
    description = ctx.get(f"service.{service_id}.description", "")
    unit = ctx.get(f"service.{service_id}.unit", "")
    city = ctx.get("company.city_for_seo", "")

    lines = [
        f"# {name} в {city}",
        "",
        description,
        "",
        f"## Когда нужна {name}",
        "",
        "- Появилась коррозия на металлических элементах.",
        "- Требуется подготовка поверхности под антикор.",
        "- Необходимо сохранить заводское ЛКП.",
        "",
        "## Как мы работаем",
        "",
        "1. Осмотр и диагностика состояния.",
        "2. Подготовка поверхности (лазерная очистка или демонтаж элементов).",
        "3. Нанесение защитных материалов.",
        "4. Контрольный осмотр и сдача работ.",
        "",
        "## Почему выбирают нас",
        "",
        "- Лазерная подготовка без абразива.",
        "- Сохранение заводского ЛКП.",
        "- Комплексная обработка скрытых полостей.",
        "- Гарантия на выполненные работы.",
        "",
        ctx.get("guarantee_notice", ""),
        "",
        ctx.get("cta_fragment", ""),
        "",
        ctx.get("contacts_fragment", ""),
    ]
    return "\n".join(lines)


def generate_page_guarantee(ctx: dict) -> str:
    city = ctx.get("company.city_for_seo", "")
    lines = [
        f"# Гарантия на антикор и лазерную очистку в {city}",
        "",
        "Мы предоставляем гарантию на выполненные антикоррозийные работы. Точные условия прописываются в договоре и зависят от вида работ, использованных материалов и условий эксплуатации автомобиля.",
        "",
        f"## {ctx.get('guarantee.workmanship.title', 'Гарантия на работы')}",
        "",
        f"Срок: {ctx.get('guarantee.workmanship.duration', 'уточняйте')}",
        "",
        "## Условия сохранения гарантии",
        "",
        "- Регулярная мойка автомобиля.",
        "- Отсутствие механических повреждений в обработанных зонах.",
        "- Своевременный контрольный осмотр.",
        "",
        "## Что не входит в гарантию",
        "",
        "- Повреждения после ДТП или механических воздействий.",
        "- Узлы и агрегаты, не входившие в перечень работ.",
        "- Скрытые дефекты, не выявленные при осмотре.",
        "",
        ctx.get("cta_fragment", ""),
        "",
        ctx.get("contacts_fragment", ""),
    ]
    return "\n".join(lines)


def generate_page_contact(ctx: dict) -> str:
    city = ctx.get("company.city_for_seo", "")
    lines = [
        f"# Контакты — Лазер Антикор в {city}",
        "",
        "## Адрес",
        "",
        f"{ctx.get('contacts.address', '')}",
        "",
        f"{ctx.get('contacts.arrival', '')}",
        "",
        "## Телефон и email",
        "",
        f"- Телефон: {ctx.get('contacts.phone', '')}",
        f"- Email: {ctx.get('contacts.email', '')}",
        "",
        "## Часы работы",
        "",
        f"{ctx.get('contacts.business_hours', '')}",
        "",
        "Работаем по предварительной записи.",
        "",
        ctx.get("cta_fragment", ""),
    ]
    return "\n".join(lines)


def generate_page_price(ctx: dict) -> str:
    city = ctx.get("company.city_for_seo", "")
    lines = [
        f"# Стоимость антикора и лазерной очистки в {city}",
        "",
        "Точная стоимость зависит от класса кузова, марки, модели, состояния автомобиля и выбранного комплекса работ. Ниже — ориентировочные цены.",
        "",
        "| Услуга | Ориентировочная цена | Единица |",
        "|--------|----------------------|---------|",
        "| Лазерная очистка ржавчины | от 12 500 ₽ | 1 м² |",
        "| Лазерная очистка краски | от 9 375 ₽ | 1 м² |",
        "| Лазерная очистка старого антикора | от 14 063 ₽ | 1 м² |",
        "| Подготовка поверхности | от 4 000 ₽ | услуга |",
        "| Нанесение цинкового грунта | от 1 000 ₽ | 1 м² |",
        "| Нанесение эпоксидного грунта | от 500 ₽ | 1 м² |",
        "| Арматурные работы | по запросу | снятие+установка |",
        "",
        "## Как получить точный расчёт",
        "",
        "1. Запишись на бесплатный осмотр.",
        "2. Мастер оценит состояние кузова и объём работ.",
        "3. Получишь детальный расчёт без скрытых доплат.",
        "",
        ctx.get("cta_fragment", ""),
        "",
        ctx.get("contacts_fragment", ""),
    ]
    return "\n".join(lines)


def generate_article_model(brand: str, model: str, ctx: dict) -> str:
    city = ctx.get("company.city_for_seo", "")
    lines = [
        f"# Антикор {brand} {model} в {city}",
        "",
        f"{brand} {model} — один из популярных автомобилей в Санкт-Петербурге. Климат с реагентами и влажностью ускоряет коррозию, особенно в скрытых зонах. Комплексная антикоррозийная обработка помогает сохранить кузов и лакокрасочное покрытие.",
        "",
        f"## Слабые места {brand} {model}",
        "",
        "- Пороги и нижние части дверей.",
        "- Арки и подкрылки.",
        "- Днище и элементы подвески.",
        "",
        "## Рекомендуемый комплекс",
        "",
        "1. Диагностика и осмотр.",
        "2. Арматурные работы (при необходимости).",
        "3. Лазерная очистка ржавчины.",
        "4. Нанесение антикоррозийных материалов.",
        "5. Консервация скрытых полостей.",
        "",
        "## Сколько стоит",
        "",
        "Точная стоимость зависит от года выпуска и состояния. Запишись на бесплатный осмотр — мастер подготовит персональный расчёт.",
        "",
        "## FAQ",
        "",
        f"**Сколько длится антикор {model}?**",
        "Обычно 1–3 дня в зависимости от объёма работ.",
        "",
        f"**Какие материалы используются для {model}?**",
        "Dinitrol, ONB Master, MasterWAX — в зависимости от зон и задач.",
        "",
        "**Гарантия сохраняется?**",
        "Да, на выполненные работы предоставляется гарантия. Точные условия — в договоре.",
        "",
        ctx.get("cta_fragment", ""),
        "",
        ctx.get("contacts_fragment", ""),
    ]
    return "\n".join(lines)


def generate_article_likbez(ctx: dict) -> str:
    city = ctx.get("company.city_for_seo", "")
    lines = [
        f"# Что такое лазерная очистка кузова в {city}",
        "",
        "## Простыми словами",
        "",
        "Лазерная очистка — это способ удалить ржавчину, старую краску, окислы и загрязнения с металла с помощью лазерного луча. В отличие от пескоструя, она не использует абразив и не истончает деталь.",
        "",
        "## Чем отличается от пескоструя",
        "",
        "- Не повреждает заводское ЛКП рядом с обрабатываемой зоной.",
        "- Не оставляет абразивной пыли.",
        "- Позволяет точечно обработать ржавчину.",
        "- Подготавливает металл под грунт и антикор.",
        "",
        "## Где применяется",
        "",
        "- Пороги, арки, днище.",
        "- Узлы подвески и рамы.",
        "- Места после мелких повреждений и сколов.",
        "",
        "## FAQ",
        "",
        "**Лазерная очистка безопасна для металла?**",
        "Да, при правильных настройках оборудования лазер удаляет только ржавчину и загрязнения, не вредя основному металлу.",
        "",
        "**Сколько стоит лазерная очистка?**",
        "Цена зависит от площади и типа покрытия. Точный расчёт — после осмотра.",
        "",
        ctx.get("cta_fragment", ""),
        "",
        ctx.get("contacts_fragment", ""),
    ]
    return "\n".join(lines)


def generate_faq_article(ctx: dict) -> str:
    city = ctx.get("company.city_for_seo", "")
    lines = [
        f"# Частые вопросы об антикоре в {city}",
        "",
        "**Сколько длится антикор?**",
        "Обычно 1–3 дня в зависимости от класса кузова и объёма работ.",
        "",
        "**Какие материалы используются?**",
        "Dinitrol, ONB Master, MasterWAX — в зависимости от зон и задач.",
        "",
        "**Нужно ли снимать элементы?**",
        "При комплексной обработке часто требуются арматурные работы — снятие и установка бамперов, подкрылков, защит.",
        "",
        "**Сохраняется ли заводская гарантия?**",
        "Антикор не влияет на заводскую гарантию, если работы выполнены корректно и не затрагивают элементы, к которым она относится.",
        "",
        "**Как записаться?**",
        "По телефону или email. Работаем по предварительной записи.",
        "",
        ctx.get("cta_fragment", ""),
        "",
        ctx.get("contacts_fragment", ""),
    ]
    return "\n".join(lines)


def save_draft(name: str, content: str, subdir: str = "Pages") -> Path:
    dest = DRAFTS_DIR / subdir
    dest.mkdir(parents=True, exist_ok=True)
    path = dest / f"{name}.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def main():
    parser = argparse.ArgumentParser(description="Generate content drafts from Knowledge")
    parser.add_argument("--service", help="Generate service page by service id")
    parser.add_argument("--brand", help="Generate model article by brand")
    parser.add_argument("--model", help="Generate model article by model")
    parser.add_argument("--all", action="store_true", help="Generate all default drafts")
    args = parser.parse_args()

    ctx = build_context()

    if args.all or not any([args.service, args.brand, args.model]):
        # Pages
        for sid in ["disassembly", "laser_cleaning", "anticor_complex", "cavity_conservation"]:
            content = generate_page_service(sid, ctx)
            path = save_draft(f"service_{sid}", content, "Pages")
            print(f"[GENERATED] {path}")

        content = generate_page_guarantee(ctx)
        path = save_draft("page_guarantee", content, "Pages")
        print(f"[GENERATED] {path}")

        content = generate_page_contact(ctx)
        path = save_draft("page_contact", content, "Pages")
        print(f"[GENERATED] {path}")

        content = generate_page_price(ctx)
        path = save_draft("page_price", content, "Pages")
        print(f"[GENERATED] {path}")

        # Articles
        for brand, model in [
            ("Toyota", "Camry"),
            ("BMW", "X5"),
            ("Lada", "Vesta"),
            ("Kia", "Rio"),
            ("Skoda", "Octavia"),
            ("Hyundai", "Creta"),
        ]:
            content = generate_article_model(brand, model, ctx)
            path = save_draft(f"article_{brand.lower()}_{model.lower()}", content, "Articles")
            print(f"[GENERATED] {path}")

        content = generate_article_likbez(ctx)
        path = save_draft("article_likbez_laser_cleaning", content, "Articles")
        print(f"[GENERATED] {path}")

        content = generate_faq_article(ctx)
        path = save_draft("article_faq_common", content, "Articles")
        print(f"[GENERATED] {path}")

    elif args.service:
        content = generate_page_service(args.service, ctx)
        path = save_draft(f"service_{args.service}", content, "Pages")
        print(f"[GENERATED] {path}")

    elif args.brand and args.model:
        content = generate_article_model(args.brand, args.model, ctx)
        path = save_draft(f"article_{args.brand.lower()}_{args.model.lower()}", content, "Articles")
        print(f"[GENERATED] {path}")


if __name__ == "__main__":
    main()
