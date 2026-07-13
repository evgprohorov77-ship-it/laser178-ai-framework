# Owner Master Profile

## Версия

1.0.0

## Назначение

Это единый файл, который владелец редактирует вручную.  
Hermes автоматически разбивает его на 5 файлов в `Owner/` и синхронизирует с `Knowledge/`.

## Как редактировать

1. Открой `Owner/MASTER_PROFILE.yaml`.
2. Измени нужные поля.
3. Скажи Hermes: **«синхронизируй мастер-профиль»**.
4. Hermes:
   - сгенерирует `company_profile.yaml`, `contacts.yaml`, `services.yaml`, `guarantees.yaml`, `pricing.yaml`;
   - синхронизирует `Knowledge/`;
   - запустит `validate_knowledge.py`.

## Правила

- Не удаляй блоки `id`, `version`, `owner_portal`, `source`.
- Для цен используй `public: true` только если цена может быть опубликована на сайте.
- Для гарантий и юридических условий — `verified: true` только после подтверждения.
