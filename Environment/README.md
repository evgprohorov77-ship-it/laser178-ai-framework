# Environment

## Среды

| Файл | Назначение |
|------|------------|
| `development.json` | Локальная разработка. Autofix P2/P3 разрешён. |
| `staging.json` | Предпрод. Autofix P2/P3 разрешён, но логируется. |
| `production.json` | Прод. Autofix запрещён по умолчанию. |
| `current.json` | Указатель на активную среду. |

## Production Lock

В `production.json` `production_lock: true`.  
Это означает: автоматические изменения запрещены, пока владелец не даст explicit override.
