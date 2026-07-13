# AI Engines

## Список движков

| Модуль | Назначение |
|--------|------------|
| `decision_engine.py` | Принимает решение по каждому Finding |
| `risk_engine.py` | Оценивает риск автоматического исправления |
| `action_engine.py` | Выполняет одобренные изменения |
| `verification_engine.py` | Проверяет результат изменения |
| `logger.py` | Логирует все шаги |

## Поток

```
Finding
  ↓
DecisionEngine.decide()
  ↓
RiskEngine.assess()
  ↓
if autofix:
  ActionEngine.execute()
  VerificationEngine.verify()
  ↓
  success: Logger.log_verification()
  fail:    rollback + Logger.log_issue()
else:
  Logger.log_issue()
```
