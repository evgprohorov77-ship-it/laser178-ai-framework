# Governance: Release Policy

## Статус

- **Действует с:** LAOS-005
- **Автор:** Owner
- **Цель:** определить правила версионирования и выпуска релизов.

## Версионирование

Используется семантическое версионирование с LAOS-спецификой:

```
vMAJOR.MINOR.PATCH
```

### v0.x — Предварительная разработка

- Архитектура может меняться без предупреждения.
- Нет обязательства обратной совместимости.
- Разрешены эксперименты, прототипы, тестовые данные.
- Подходит для стадии до LAOS Core Feature Freeze.
- **Текущий статус:** LAOS закончил v0.x и перешёл к стабилизации.

### v1.x — Стабильная версия

- Обратная совместимость обязательна.
- Изменения Knowledge и Governance не ломают существующие скрипты и процессы.
- Minor-релизы добавляют новые сущности, контент, улучшения без breaking changes.
- Patch-релизы — исправления, уточнения, верификация данных.
- Любой релиз v1.x требует owner approval.

### v2.x — Только через RFC

- Major-релизы (v2.x и выше) возможны только через утверждённый RFC.
- Breaking changes разрешены, но должны быть явно описаны и согласованы.
- Переход на v2.x требует миграции данных и approval Owner.

## Типы релизов

| Тип | Когда | Пример | Требования |
|-----|-------|--------|------------|
| Patch | Исправление, верификация, уточнение | v1.0.1 | validate_knowledge.py проходит, owner approval для production-изменений. |
| Minor | Новый контент, новая сущность Knowledge, улучшение инструментов | v1.1.0 | validate_knowledge.py проходит, review, owner approval. |
| Major | Breaking changes, новая архитектура | v2.0.0 | RFC, миграция, owner approval. |
| Hotfix | Critical incident | v1.0.1-hotfix | incident_response.md, owner notification, post-fix review. |

## Процесс релиза

1. Сформировать scope релиза из approved RFC и задач.
2. Обновить версию в `pyproject.toml` или `version.txt`.
3. Запустить `validate_knowledge.py`.
4. Запустить `check_content.py` для всех draft-статей.
5. Owner даёт approval.
6. Создать Git tag.
7. Записать Changelog entry.
8. При необходимости — применить изменения к production через approved процедуру.

## Обратная совместимость

- v1.x обязана поддерживать старые YAML-файлы Knowledge.
- Если схема меняется, добавляется миграция в `Scripts/migrate/`.
- Миграция не ломает данные Owner.

## Changelog

- Каждый релиз фиксируется в `Changelog/<version>.md`.
- Запись содержит:
  - версию;
  - дату;
  - список изменений;
  - автора/роль;
  - статус verification;
  - примечания о breaking changes.

## Примечания

- Пока LAOS Core в Feature Freeze, новые версии будут веткой v1.x.
- WordPress Adapter не может быть частью v1.x без завершения Security Layer и тестового стенда.
- Owner может в любой момент откатить релиз через Git revert или restore from backup.
