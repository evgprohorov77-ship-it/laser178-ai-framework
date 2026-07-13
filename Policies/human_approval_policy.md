# Human Approval Policy

## Версия

1.0.0

## Цель

Любое потенциально опасное или важное действие требует явного одобрения человека.

## Когда требуется approval

| Условие | Требуется approval |
|---------|-------------------|
| Severity P0 | Да |
| Severity P1 | Да |
| Environment = production | Да, кроме readonly |
| Confidence < 0.70 | Да, даже если P2/P3 |
| Изменение затрагивает >N страниц | Да |
| Изменение файлов/БД/плагинов | Да |
| Отсутствует rollback | Да |
| Owner override активирован | Да, override — это форма approval |

## Структура approval

```json
{
  "uuid": "...",
  "title": "...",
  "description": "...",
  "reason": "...",
  "risks": [...],
  "rollback_plan": {...},
  "target_url": "...",
  "proposed_changes": [...],
  "requested_by": "agent",
  "requested_at": "...",
  "status": "waiting",
  "approved_by": null,
  "approved_at": null,
  "expires_at": "...",
  "dry_run_uuid": "..."
}
```

## Статусы

- `waiting` — ожидает решения владельца.
- `approved` — одобрено, можно выполнять.
- `rejected` — отклонено, действие не выполняется.
- `expired` — не получено решение в срок.

## Срок действия

Approval действителен 24 часа. После истечения требуется новый Dry Run.

## Канал доставки

- Telegram.
- Email.
- GitHub issue (fallback).

## Без approval — нет действия

Authorization Engine отказывает в любом действии без действующего approval, если оно требуется.
