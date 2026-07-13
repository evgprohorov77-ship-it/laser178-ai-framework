# Production Policy

## Версия

1.0.0

## Статус

Production Lock = **ACTIVE** по умолчанию.

## Правило

В production автоматические изменения запрещены.

## Что запрещено в production

- autofix любого severity;
- изменение файлов через Action Engine;
- изменение базы данных WordPress;
- создание/удаление страниц;
- изменение плагинов;
- изменение темы;
- изменение `.htaccess`, `wp-config.php`;
- любое действие без explicit owner override.

## Что разрешено в production

- Аудит (readonly).
- Создание отчётов.
- Создание approval requests (без выполнения).
- Создание issues.
- Чтение Knowledge.

## Production override

Owner может активировать override на конкретное действие:

```
override = {
  "approval_uuid": "...",
  "target": "https://laser178.ru/",
  "action": "edit_title",
  "expires": "2026-07-13T18:00:00Z",
  "owner": "..."
}
```

Override:

- имеет TTL;
- привязан к approval UUID;
- логируется отдельно;
- не распространяется на P0.

## Разделение сред

| Среда | Назначение |
|-------|------------|
| development | Локальные эксперименты. Autofix P2/P3 разрешён. |
| staging | Проверка перед продом. Autofix P2/P3 разрешён, но логируется. |
| production | Только readonly и owner-approved действия. |

## Переключение среды

LAOS определяет среду через `Environment/current.json`.  
Переключение в production требует подтверждения владельца.
