# Authorization Engine

## Версия

1.0.0

## Назначение

Отвечает только на один вопрос: **«Можно ли выполнить действие?»**

Не решает, как выполнять. Это задача Action Engine.

## Проверки

1. Environment существует.
2. Production Lock не активен.
3. Capability включена.
4. Severity разрешена (P2/P3).
5. Confidence ≥ 0.70.
6. Approval получен, если требуется.
7. Backup присутствует, если rollback required.
8. Dry Run выполнен.
9. Framework reference существует.

## Результат

```python
{
  "allowed": true | false,
  "reason": "...",
  "checks": [...]
}
```

## Использование

См. `Scripts/run_laos.py`.
