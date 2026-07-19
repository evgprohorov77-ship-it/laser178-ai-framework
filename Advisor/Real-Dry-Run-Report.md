# LAOS-011 — External Advisor Mode v1.1 Real Dry Run Report

## Дата проведения

2026-07-19

## Цель

Провести один реальный запрос к OpenAI Responses API через модуль `Advisor`, проверить безопасность, санитизацию, схему ответа и логирование.

## 1. Проверка кода

| Проверка | Результат |
|----------|-----------|
| Используется OpenAI Responses API | ✅ `client.responses.create(...)` |
| API key читается только из `OPENAI_API_KEY` | ✅ `os.environ.get("OPENAI_API_KEY")` |
| Ключ не выводится в stdout/stderr/логи | ✅ В логи попадает только `model`, `verdict`, `confidence`, `usage` |
| `config.yaml` исключён из Git | ✅ Добавлен в `.gitignore` |
| `.env` исключён из Git | ✅ Уже был в `.gitignore` |
| Git history не содержит секретов | ✅ `git log -S` не нашёл `sk-`, `password=`, `token=` |
| Git status чистый от секретов | ✅ только `.gitignore` и `Advisor/advisor.py` |

## 2. Конфигурация dry run

Создан локальный файл `Advisor/config.yaml` (не коммитится):

```yaml
advisor:
  enabled: false          # возвращено в false после проверки
  model: "gpt-4.1-nano"
  max_context_chars: 4000
  max_output_tokens: 1200
  daily_request_limit: 3
  timeout: 30
```

`config.example.yaml` оставлен без изменений.

## 3. Тестовый запрос

| Поле | Значение |
|------|----------|
| task_id | `LAOS-ADVISOR-V1.1-DRYRUN` |
| review_type | `ux_review` |
| question | Оцени мобильную версию главной страницы laser178.ru и предложи не более пяти улучшений |
| proposed_solution | Текущая мобильная версия: hero, CTA, фиксированная нижняя панель, темная тема, калькуляторы |
| risk_level | `LOW` |

## 4. Санитизация контекста

Файлы сохранены локально, не коммитятся:

- `Advisor/context_before_sanitization.txt`
- `Advisor/context_after_sanitization.txt`

### Проверка diff

В `before` были вставлены тестовые секреты:

- `OPENAI_API_KEY should be removed if present`
- `email like owner@laser178.ru`
- `phone +7 999 123-45-67`

В `after` они заменены на:

- `[REDACTED_API_KEY]`
- `[REDACTED_EMAIL]`
- `[REDACTED_PHONE]`

### Результат проверки safety

```text
PASS: no secrets/PII detected in sanitized context
```

## 5. Реальный запрос к OpenAI

### Блокер

`OPENAI_API_KEY` **не установлен в окружении сервера**.

Проверены места:

- переменная окружения текущей сессии — отсутствует;
- `/root/.hermes/.env` — ключ не найден;
- `.bashrc`, `.profile`, `/etc/environment` — ключ не найден.

### Результат вызова

```json
{
  "verdict": "advisor_unavailable",
  "summary": "Advisor unavailable: advisor_unavailable: OPENAI_API_KEY not set. Hermes must proceed according to Policy Layer.",
  "strengths": [],
  "issues": ["advisor_unavailable: OPENAI_API_KEY not set"],
  "recommendations": ["Request owner decision if risk is HIGH."],
  "risks": ["No external review was obtained."],
  "confidence": 0.0,
  "requires_owner_decision": false
}
```

### Исправленный баг

При отсутствии кода Advisor падает с `RuntimeError`. В процессе dry run исправлено на корректный fallback `advisor_unavailable`. Все 25 unit-тестов проходят.

## 6. Проверка JSON Schema и логов

Поскольку реальный запрос не выполнен, валидация схемы проведена на fallback-ответе.

| Проверка | Результат |
|----------|-----------|
| Fallback JSON соответствует `advisor_response.schema.json` | ✅ |
| `verdict` допустимое (`advisor_unavailable`) | ✅ |
| `confidence` в диапазоне 0–1 | ✅ (0.0) |
| `recommendations` — массив | ✅ |
| usage не записан (не было запроса) | ✅ |
| Полный контекст не попал в логи | ✅ |
| В логи попал только `task_id` и причина ошибки | ✅ |

## 7. Найденные проблемы

| # | Проблема | Уровень | Статус |
|---|----------|---------|--------|
| 1 | `OPENAI_API_KEY` не установлен в окружении | Блокер | Требуется действие Owner |
| 2 | При отсутствии кода Advisor падал с RuntimeError | Средний | ✅ Исправлено на fallback |
| 3 | `config.yaml` не был в `.gitignore` | Низкий | ✅ Исправлено |
| 4 | Dry-run артефакты могли попасть в Git | Низкий | ✅ Добавлены в `.gitignore` |

## 8. Рекомендация

**Интеграция Advisor в Hermes пока не разрешена.**

Причина: не проведён успешный реальный запрос к OpenAI. Без него нельзя гарантировать, что:

- модель корректно понимает промпты;
- JSON-ответ валиден и полезен;
- стоимость и latency в пределах допустимых;
- санитизация работает на реальном входе.

### Что нужно сделать Owner

1. Добавить `OPENAI_API_KEY` в окружение сервера (например, в `/root/.hermes/.env` или `export` в текущей сессии).
2. **Не передавать ключ в Telegram или другие чаты.**
3. Повторно запросить у меня `LAOS TASK — External Advisor Mode v1.1 Real Dry Run`.
4. Я выполню один реальный запрос и подготовлю полный отчёт.

## 9. Последствия

- `Advisor/config.yaml` возвращён в `enabled: false`.
- Advisor **не интегрирован** в автоматический процесс Hermes.
- Второй запрос без разрешения Owner не выполнялся.
- Работа остановлена.
