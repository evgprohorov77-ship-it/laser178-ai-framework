# Owner Fact Verification

## Статус

- **Этап:** LAOS-004
- **Цель:** владелец подтверждает факты из Knowledge DB.
- **Ограничения:**
  - Не создавать новые Engines, Adapters или архитектурные слои.
  - Не подключать WordPress API.
  - Не выполнять реальные изменения production-сайта.
  - Не удалять старые Knowledge-файлы без подтверждения.

## Анкеты

| Анкета | Файл | Статус |
|--------|------|--------|
| Company + Contacts | `anketa_company_contacts.md` | отправлена владельцу |
| Guarantees | `anketa_guarantees.md` | подготовлена |
| Services + Prices | `anketa_services_prices.md` | подготовлена |

## Процесс

1. Подготовить анкету по текущим YAML.
2. Показать владельцу.
3. После ответа обновить YAML.
4. Запустить `python3 Scripts/validate_knowledge.py`.
5. Зафиксировать в `verification` статус: `pending`, `partial`, `complete`.

## Правила записи фактов

- `verified: true` только после ответа владельца или официального документа.
- `source` обязателен.
- `null` или `needs_verification` — допустимые значения для неподтверждённых полей.
- Публичный текст сайта не считается достаточным для юридических, гарантийных и ценовых условий.

## Архивация старых .md

Старые `.md` из `Knowledge/Company/` переносятся в `Archive/Knowledge-Legacy/` только после:
- сравнения с YAML;
- подтверждения владельца;
- фиксации в CHANGELOG.

## Исследование конкурентов

Не добавляется в `Knowledge/Company/`. Хранится в `Research/Competitors/` с датами и источниками.
