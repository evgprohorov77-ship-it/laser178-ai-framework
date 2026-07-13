# Owner Portal

## Версия

1.0.0

## Назначение

Owner Portal — это единственное место, где владелец редактирует данные компании.  
Hermes автоматически:
- валидирует файлы Owner Portal;
- синхронизирует их в `Knowledge/`;
- обновляет статьи и FAQ на основе новых данных.

## Структура

| Файл | Что редактирует Owner | Куда синхронизируется |
|------|------------------------|------------------------|
| `company_profile.yaml` | Бренд, юр. лицо, регион, миссия, УТП, ЦА | `Knowledge/Company/company.yaml` |
| `contacts.yaml` | Телефон, email, адрес, часы, мессенджеры | `Knowledge/Company/contacts.yaml` |
| `services.yaml` | Услуги, описания, единицы, пакеты | `Knowledge/Company/services.yaml` |
| `guarantees.yaml` | Гарантии, сроки, условия, исключения | `Knowledge/Company/guarantees.yaml` |
| `pricing.yaml` | Цены, коэффициенты, материалы, округление | `Knowledge/Company/prices.yaml`, `materials.yaml` |

## Процесс работы

1. Owner редактирует нужный `Owner/*.yaml`.
2. Hermes запускает `Scripts/sync_owner_to_knowledge.py`.
3. Скрипт:
   - парсит Owner YAML;
   - проверяет структуру;
   - обновляет соответствующие файлы в `Knowledge/`;
   - запускает `validate_knowledge.py`;
   - генерирует diff для review.
4. Owner review и approval.
5. Hermes обновляет статьи и FAQ (draft) на основе новых данных.
6. Публикация только после owner approval.

## Правила

- Owner редактирует только файлы в `Owner/`.
- Hermes не меняет `Owner/*.yaml` без просьбы Owner.
- `Knowledge/` — производная от `Owner/` + валидация.
- Никакие production-изменения без owner approval.

## Примеры

См. `Owner/template.yaml` и README в каждом файле.
