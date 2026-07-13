# Approval Manager

## Версия

1.0.0

## Назначение

Хранит и управляет approval requests от агента к владельцу.

## Статусы

- `waiting` — ожидает решения.
- `approved` — одобрено.
- `rejected` — отклонено.
- `expired` — срок истёк.

## Структура

См. `approval_manager.py`.

## Срок действия

24 часа. После — требуется новый Dry Run.
