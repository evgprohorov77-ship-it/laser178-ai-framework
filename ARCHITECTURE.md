# Архитектура репозитория LAOS

## Принцип

Репозиторий разделён на три зоны:

1. **AI/** — исполнительная система агента.
2. **Framework/** — правила, роли, стандарты.
3. **Auditors/** — детекторы проблем.

Такое разделение отражает разделение ответственности: *что делать* (Framework), *кто решает* (AI), *что проверяет* (Auditors).

## Новая структура

```
laser178-ai-framework/
├── AI/                             # Исполнительная система
│   ├── Decision/                   # Decision Engine
│   │   ├── README.md
│   │   ├── AI_DECISION_ENGINE.md
│   │   └── decision_engine.py
│   ├── Engines/                    # Остальные движки
│   │   ├── README.md
│   │   ├── action_engine.py
│   │   ├── risk_engine.py
│   │   ├── verification_engine.py
│   │   └── logger.py
│   └── Models/                     # Единые модели данных
│       └── finding.py
│
├── Auditors/                       # Детекторы проблем
│   ├── README.md
│   ├── base_auditor.py
│   ├── runner.py
│   ├── seo_auditor.py
│   ├── structure_auditor.py
│   ├── images_auditor.py
│   ├── performance_auditor.py
│   ├── security_auditor.py
│   └── wordpress_auditor.py
│
├── Framework/                      # Правила и стандарты
│   ├── zones.md
│   ├── roles.md
│   └── quality-checklist.md
│
├── Knowledge/                      # База знаний о компании
│   └── company.md
│
├── Policies/                       # Политики
│   ├── rollback_policy.md
│   ├── severity_and_confidence.md
│   └── framework_reference.md
│
├── Registry/                       # Реестр правил
│   └── rules.json
│
├── Operations/                     # SOP и вспомогательные скрипты
│   ├── backup-sop.md
│   └── audit.py                    # deprecated, оставлен для истории
│
├── Scripts/                        # Entrypoints
│   └── run_laos.py
│
├── Tests/                          # Тесты
│
├── Logs/                           # Логи (в .gitignore)
│   └── .gitkeep
│
├── .github/                        # Шаблоны issue
│   └── ISSUE_TEMPLATE/
│
├── README.md
├── .gitignore
└── AI_DECISION_ENGINE.md           # symlink / копия в корне для удобства
```

## Преимущества каждого изменения

| Изменение | Почему |
|-----------|--------|
| `AI/Decision/` | Decision Engine — центральный компонент, достоин отдельной директории. |
| `AI/Engines/` | Risk, Action, Verification — модули одного уровня, но не центральны. |
| `AI/Models/` | Единая модель `Finding` исключает произвольные структуры. |
| `Auditors/` | Каждый аудитор отвечает только за свою область. |
| `Policies/` | Severity, rollback, framework reference — политики, а не код. |
| `Registry/` | Реестр правил отделён от документов, позволяет валидировать `framework_reference`. |
| `Scripts/` | Entrypoint `run_laos.py` — единый способ запуска всей системы. |
| `Tests/` | Место для unit-тестов аудиторов и Decision Engine. |
| `Logs/` | Логи хранятся вне кода, но в репо есть `.gitkeep`. |

## Устаревшие файлы

- `Operations/audit.py` — оставлен как исторический артефакт. Новый аудит запускается через `Scripts/run_laos.py`.

## Правила добавления нового аудитора

1. Создать `Auditors/{name}_auditor.py`.
2. Наследовать `BaseAuditor`.
3. Реализовать `audit(url, html, headers) -> List[Finding]`.
4. Добавить правило в `Registry/rules.json`.
5. Добавить документ в `Framework/` или `Policies/` при необходимости.
6. Добавить тест в `Tests/`.

## Правила добавления нового действия Action Engine

1. Добавить тип в `ActionEngine.supported_actions`.
2. Реализовать инструкцию в `_generate_instructions`.
3. Добавить rollback-план в `Policies/rollback_policy.md`.
4. Добавить verification в `VerificationEngine.verify`.
