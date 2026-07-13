# LAOS — Laser178 AI Operating System

## Статус

- **LAOS Core:** Feature Freeze (LAOS-005)
- **Версия:** v1.0.0
- **Автор:** Евгений Прохоров + Hermes

## Описание

LAOS — цифровой инженер компании «Лазер Антикор».  
Система управляет знаниями, контентом и изменениями сайта laser178.ru через проверенную базу знаний и governance-процессы.

## Ключевые принципы

1. **LAOS Core завершён.** Новые Engines и Adapters не создаются.
2. **WordPress REST API не используется.** См. `RFC/0002-wordpress-adapter.md`.
3. **Production изменения только после owner approval.**
4. **Owner Portal — единственный источник правды для бизнес-данных.**
5. **Knowledge DB — производная от Owner Portal + валидация.**
6. **Любое изменение проходит через RFC → Review → Approval → Implementation → Verification → Release → Changelog.**
7. **Публичный текст сайта не является достаточным источником для цен, гарантий и юридических условий.**

## Быстрый старт

### Для Owner

1. Редактируй файлы в `Owner/`.
2. Скажи Hermes: **«синхронизируй Owner Portal»**.
3. Hermes обновит `Knowledge/` и запустит валидацию.
4. Review diff и дай approve.
5. Hermes подготовит контент (статьи, FAQ), но не опубликует без approval.

### Для разработчика/Operator

```bash
python3 Scripts/validate_knowledge.py
python3 Scripts/check_content.py path/to/article.md
python3 Scripts/sync_owner_to_knowledge.py --dry-run
python3 Scripts/sync_owner_to_knowledge.py
```

## Структура репозитория

```
laser178-ai-framework/
├── .hermes/                  # Конфигурация Hermes
├── Archive/                  # Архив legacy-файлов (только после owner approval)
├── Audit/                    # Аудиторские записи
├── Changelog/                # История изменений по версиям
├── Content/                  # Контент, статьи, FAQ (draft)
├── Governance/               # Governance Layer
│   ├── README.md
│   ├── roles.md
│   ├── permissions.md
│   ├── approval_matrix.md
│   ├── change_management.md
│   ├── release_policy.md
│   ├── versioning_policy.md
│   ├── incident_response.md
│   └── audit_policy.md
├── Knowledge/                # База знаний (производная от Owner Portal)
│   ├── README.md
│   ├── schema.md
│   └── Company/
│       ├── template.md
│       ├── company.yaml
│       ├── contacts.yaml
│       ├── services.yaml
│       ├── materials.yaml
│       ├── equipment.yaml
│       ├── prices.yaml
│       ├── faq.yaml
│       ├── guarantees.yaml
│       ├── partners.yaml
│       ├── cars.yaml
│       ├── employees.yaml
│       └── legal.yaml
├── Owner/                    # Owner Portal (editable)
│   ├── README.md
│   ├── template.md
│   ├── company_profile.yaml
│   ├── contacts.yaml
│   ├── services.yaml
│   ├── guarantees.yaml
│   └── pricing.yaml
├── Research/                 # Исследования
│   └── Competitors/
├── RFC/                      # Request for Change
├── Scripts/                  # Валидаторы и синхронизация
│   ├── validate_knowledge.py
│   ├── check_content.py
│   └── sync_owner_to_knowledge.py
├── ARCHITECTURE.md
├── README.md
└── version.txt
```

## Приоритеты

1. **Knowledge — №1.** Наполнение и верификация данных.
2. **Governance — №2.** Процессы, роли, утверждения.
3. **Практическое применение на laser178.ru — №3.**
4. **WordPress Adapter — только после Security Layer и тестового стенда.**

## Безопасность

- Production Lock активен по умолчанию.
- Capability `security` отключена до завершения Security Layer.
- Все автоматические изменения в production требуют owner approval.
- Dry Run и review обязательны перед любым релизом.
- Hermes не хранит и не получает credentials, пароли, API-ключи.

## Лицензия

Собственность ИП Прохоров Е.А. Использование только в рамках laser178.ru.

## Контакты

- Сайт: https://laser178.ru
- Email: info@laser178.ru
- Telegram: DM с Евгением Прохоровым
