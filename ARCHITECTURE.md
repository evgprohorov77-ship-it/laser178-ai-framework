# LAOS Architecture

## Версия

1.1.0

## Общее описание

LAOS состоит из трёх слоёв:

1. **Owner Portal** — интерфейс владельца для редактирования бизнес-данных.
2. **Knowledge Layer** — проверенная база знаний, производная от Owner Portal.
3. **Governance Layer** — процессы, роли, утверждения, релизы, аудит.

## Схема данных

```
Owner Portal (Owner редактирует)
       ↓
Scripts/sync_owner_to_knowledge.py (валидирует + синхронизирует)
       ↓
Knowledge Layer (YAML DB)
       ↓
Scripts/generate_content.py + Content Templates
       ↓
Content Drafts (страницы, статьи, FAQ)
       ↓
Scripts/check_content.py (проверка на verified факты)
       ↓
Owner Approval
       ↓
Production (WordPress, FTP) — только после Security Layer + test stand
```

## Компоненты

### Owner Portal

- `Owner/company_profile.yaml` → `Knowledge/Company/company.yaml`
- `Owner/contacts.yaml` → `Knowledge/Company/contacts.yaml`
- `Owner/services.yaml` → `Knowledge/Company/services.yaml`
- `Owner/guarantees.yaml` → `Knowledge/Company/guarantees.yaml`
- `Owner/pricing.yaml` → `Knowledge/Company/prices.yaml` + `materials.yaml`

### Knowledge Layer

- Единая схема: `Knowledge/schema.md`.
- Валидатор: `Scripts/validate_knowledge.py`.
- Каждый YAML-файл имеет `id`, `version`, `entity_type`, `status`, `verification`.
- Все факты имеют `value`, `verified`, `source`, `public` (для Owner-derived) или `value`, `verified`, `source` (для Knowledge).

### Governance Layer

См. `Governance/README.md`. Основные документы:
- `roles.md` — роли.
- `permissions.md` — права.
- `approval_matrix.md` — матрица утверждений.
- `change_management.md` — процесс изменений.
- `release_policy.md` — релизы и версии.
- `versioning_policy.md` — версионирование компонентов.
- `incident_response.md` — инциденты.
- `audit_policy.md` — аудит.

## Структура репозитория

```
laser178-ai-framework/
├── .hermes/
├── Archive/
├── Audit/
├── Changelog/
├── Content/
├── Content/                  # Content Layer
│   ├── README.md
│   ├── Templates/            # Шаблоны страниц и статей
│   ├── Drafts/               # Черновики, сгенерированные Hermes
│   ├── Published/            # Утверждённые и опубликованные материалы
│   └── Fragments/            # CTA, контакты, гарантийные вставки
├── Governance/           ← Governance Layer
├── Knowledge/              ← Knowledge Layer
│   ├── schema.md
│   └── Company/
├── Owner/                  ← Owner Portal
├── Research/
│   └── Competitors/
├── RFC/
├── Scripts/
│   ├── validate_knowledge.py
│   ├── check_content.py
│   └── sync_owner_to_knowledge.py
├── ARCHITECTURE.md
├── README.md
└── version.txt
```

## Change Management

```
Идея / Запрос
      ↓
   RFC
      ↓
   Review
      ↓
   Approval
      ↓
   Implementation
      ↓
   Verification
      ↓
   Release
      ↓
   Changelog
```

## Версионирование

- LAOS Core: `vMAJOR.MINOR.PATCH` в `version.txt`.
- Knowledge Schema: отдельная версия в `Knowledge/schema.md`.
- Owner Portal: `Owner/README.md` → версия.
- Governance: версия в каждом документе.
- Скрипты: `__version__` в каждом.

## Release Policy

- **v0.x** — эксперименты, breaking changes разрешены.
- **v1.x** — обратная совместимость обязательна. Текущий статус.
- **v2.x+** — только через RFC, breaking changes согласованы.

## Security Layer

- **Статус:** не реализован.
- **Зависимости:** WordPress Adapter, production access, secrets management.
- **Условие запуска:** завершение Security Layer и успешная эксплуатация на тестовом стенде.

## Запреты

- Не создавать новые Engines или Adapters в Feature Freeze.
- Не подключать Production без owner approval.
- Не использовать WordPress REST API до Security Layer.
- Не удалять старые `.md` из `Knowledge/Company/` без owner approval и архивации.
- Не хранить credentials в репозитории.

## Приоритеты

1. Knowledge — №1.
2. Governance — №2.
3. Практическое применение на laser178.ru — №3.
4. WordPress Adapter — после Security Layer + test stand.

## Безопасность

- Production Lock активен по умолчанию.
- Capability `security` отключена до завершения Security Layer.
- Все автоматические изменения в production требуют owner approval.
- Dry Run и review обязательны перед любым релизом.
- Hermes не хранит и не получает credentials, пароли, API-ключи.

## Следующие шаги

1. Наполнение Owner Portal реальными данными.
2. Синхронизация с Knowledge.
3. Генерация SEO-контента через `Scripts/generate_content.py`.
4. Review и owner approval.
5. Ручная публикация на laser178.ru или через WordPress Adapter после Security Layer.
6. Security Layer и тестовый стенд для WordPress Adapter.
