# Decision Engine

## Назначение

Decision Engine — центральный компонент LAOS. Он принимает **Finding** от аудиторов, оценивает его по матрице рисков и решает:

- исправлять автоматически;
- запрашивать подтверждение владельца;
- создавать GitHub Issue;
- отклонить как ложное срабатывание.

## Поток данных

```
Auditor → Finding
   ↓
Decision Engine
   ↓
Risk Engine
   ↓
Action Engine (если autofix == true)
   ↓
Verification Engine
   ↓
Logging
   ↓
GitHub Issue (только если исправление невозможно или отклонено)
```

## Ключевые принципы

1. **Framework-Reference** обязателен. Если для Finding нет ссылки на правило — создаётся Issue «Framework Improvement».
2. **Confidence < 0.70** → автоматическое исправление запрещено.
3. **P0** → автоматическое исправление запрещено всегда.
4. **P1** → требуется подтверждение владельца.
5. **P2/P3** → допускается autofix, если `rollback_required == false` или rollback возможен.
6. **Любое изменение отвечает на вопрос**: «Что конкретно станет лучше?» Если ответ отсутствует — изменение запрещено.

## Правила принятия решений

| Severity | Confidence | Autofix | Решение |
|----------|------------|---------|---------|
| P0 | любая | любой | Создать Issue, запретить autofix. |
| P1 | любая | любой | Запросить подтверждение владельца. |
| P2 | ≥ 0.70 | true | Выполнить autofix, затем verify. |
| P2 | < 0.70 | true | Создать Issue. |
| P3 | ≥ 0.70 | true | Выполнить autofix, если rollback есть. |
| P3 | < 0.70 | любой | Создать Issue или отклонить. |

## Интерфейс

Метод `decide(finding: Finding) -> Decision`.

Возвращает объект:

```json
{
  "action": "autofix|ask|issue|reject",
  "reason": "string",
  "assigned_engine": "action_engine|none",
  "requires_rollback": true|false,
  "owner_prompt": null|string
}
```

## Расположение

`AI/Decision/decision_engine.py` — реализация.
`AI/Decision/README.md` — этот документ.
`AI/Decision/AI_DECISION_ENGINE.md` — детальная спецификация.
