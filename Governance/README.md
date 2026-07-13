# Governance

## Статус

- **Действует с:** LAOS-005
- **Цель:** управлять изменениями, правами, релизами и рисками LAOS.

## Документы

| Документ | Назначение |
|----------|------------|
| `roles.md` | Роли и обязанности |
| `permissions.md` | Права доступа по ролям и областям |
| `approval_matrix.md` | Кто утверждает какие изменения |
| `change_management.md` | Процесс от идеи до релиза |
| `release_policy.md` | Правила версионирования и релизов |
| `versioning_policy.md` | Версионирование компонентов |
| `incident_response.md` | Действия при инцидентах |
| `audit_policy.md` | Что фиксируется и как проверяется |

## Принципы

1. **Owner — единственный источник утверждения** для production, цен, гарантий, юридических условий и контактов.
2. **Hermes не публикует автоматически** и не имеет доступа к production без approval.
3. **Любое изменение** проходит через review, approval, implementation, verification, release, changelog.
4. **LAOS Core — Feature Freeze.** Новые Engines и Adapters запрещены.

## Версия

1.0.0
