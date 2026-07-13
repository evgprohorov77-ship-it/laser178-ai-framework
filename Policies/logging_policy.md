# Logging Policy

## Версия

1.0.0

## Цель

Каждое действие LAOS должно быть записано, чтобы его можно было аудировать и воспроизвести.

## Что логируется

| Событие | Данные |
|---------|--------|
| audit | URL, аудитор, найденные Finding, timestamp. |
| decision | rule_id, decision, reason, confidence, risk. |
| authorization | request, allowed, reason, environment, capability. |
| approval | approval UUID, status, owner, timestamp, expiry. |
| dry_run | план изменений, предполагаемый результат, риски. |
| backup | backup UUID, target, hash, status. |
| action | что изменено, где, до/после. |
| verification | status, checks, before/after. |
| rollback | backup UUID, причина, результат. |
| issue | issue number, reason, fallback. |
| error | traceback, severity, retry policy. |

## Требования

1. Логи хранятся в `Logs/{session_id}/`.
2. Каждый лог — JSON Line.
3. Время в UTC.
4. UUID для каждой сессии.
5. Логи не удаляются автоматически.
6. Логи доступны только владельцу и администратору.
7. Каждый лог связан с `approval_uuid` и `backup_uuid`.

## Формат

```json
{
  "timestamp": "2026-07-13T12:00:00Z",
  "event": "action",
  "session_id": "...",
  "approval_uuid": "...",
  "backup_uuid": "...",
  "finding_id": "...",
  "details": {}
}
```

## Ротация

- Логи разбиваются по сессии.
- Старые сессии архивируются после 90 дней.
- Размер одного лог-файла не более 50 МБ.

## Безопасность

В логах не хранятся:

- пароли;
- API-токены;
- SSH-ключи;
- личные данные клиентов.
