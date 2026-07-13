# Template: Страница контактов

## Структура

1. H1 — «Контакты — Лазер Антикор в {{region}}»
2. Адрес + схема въезда
3. Телефон, email, мессенджеры (только public)
4. Часы работы + запись
5. Карта (placeholder)
6. CTA

## Правила

- Использовать только `public: true` данные из `Knowledge/Company/contacts.yaml`.
- Если мессенджер не public — не публиковать.
- Адрес и схема въезда — обязательно.

## Placeholder

```markdown
# Контакты — Лазер Антикор в {{company.city_for_seo}}

## Адрес

{{contacts.address}}

{{contacts.arrival}}

## Телефон и email

- Телефон: {{contacts.phone}}
- Email: {{contacts.email}}

## Часы работы

{{contacts.business_hours}}

Работаем по предварительной записи.

{{cta_fragment}}
```
