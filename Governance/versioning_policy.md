# Governance: Versioning Policy

## Статус

- **Действует с:** LAOS-005
- **Автор:** Owner
- **Цель:** стандартизировать, как версионируются компоненты LAOS.

## Уровни версионирования

### 1. LAOS Core

- Версия проекта в целом: `vMAJOR.MINOR.PATCH`.
- Хранится в `version.txt` или `pyproject.toml`.
- Управляется `Governance/release_policy.md`.

### 2. Knowledge DB

- Версия схемы: `Knowledge/schema.md` → `version: X.Y.Z`.
- Каждый YAML-файл имеет `version: "X.Y.Z"`.
- При изменении схемы обновляется версия схемы и всех затронутых файлов.

### 3. Owner Portal

- Версия шаблонов: `Owner/README.md`.
- Синхронизация с Knowledge версионируется через Git commit.

### 4. Governance

- Версия каждого документа: заголовок `## Версия` внутри `.md`.
- Изменения политик — minor или major в зависимости от impact.

### 5. Scripts

- Каждый скрипт имеет `__version__`.
- Breaking changes — major bump.
- Новые фичи — minor bump.
- Исправления — patch bump.

### 6. Content

- Статьи версионируются через Git history.
- Каждая публикация — отдельный commit.
- Драфты не имеют версии, пока не утверждены.

## Правила обновления версий

| Ситуация | Какую версию менять | На сколько |
|----------|---------------------|------------|
| Исправление опечатки в Knowledge | Patch в файле + Patch в схеме* | +0.0.1 |
| Новая verified сущность в Knowledge | Minor в файле + Minor в схеме | +0.1.0 |
| Breaking change в схеме Knowledge | Major в схеме + все файлы | +1.0.0 |
| Новый Governance-документ | Minor LAOS Core | +0.1.0 |
| Изменение ролей/permissions | Minor LAOS Core | +0.1.0 |
| New Engine/Adapter | Major LAOS Core (запрещено в Feature Freeze) | +1.0.0 |
| Production release | Patch/Minor/Major LAOS Core | по impact |
| Hotfix | Patch + hotfix-tag | +0.0.1 |

\* Если опечатка не меняет структуру, схема может не меняться.

## Формат версий

- `v1.0.0` — стабильный релиз.
- `v1.0.1` — патч.
- `v1.1.0` — minor.
- `v2.0.0` — major breaking change.
- `v1.0.1-hotfix-20260713` — hotfix.

## Где хранить версии

```
laser178-ai-framework/
├── version.txt                 # LAOS Core version
├── pyproject.toml              # LAOS Core version (если Python-пакет)
├── Knowledge/
│   ├── schema.md               # Knowledge Schema version
│   └── Company/
│       └── *.yaml              # per-file version
├── Governance/
│   └── *.md                    # per-document version
├── Owner/
│   └── README.md               # Owner Portal version
└── Scripts/
    └── *.py                    # per-script __version__
```

## Совместимость

- v1.x Knowledge файлы совместимы с v1.x схемы.
- v2.x схема может требовать миграцию v1.x файлов.
- Скрипты v1.x поддерживают Knowledge v1.x.
- Owner Portal версионируется отдельно и не ломает Knowledge.

## Примечание

LAOS Core сейчас в Feature Freeze. Все версии после LAOS-005 — v1.x, пока Owner не примет решение о major переходе через RFC.
