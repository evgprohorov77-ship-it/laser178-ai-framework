# Laser178 AI Operating System (LAOS)

AI-агент для управления сайтом `laser178.ru`. Работает как команда специалистов: технический директор, SEO-специалист, редактор, контент-менеджер, WordPress-разработчик, QA-инженер, веб-мастер, аналитик.

## Архитектура

LAOS построена вокруг Decision Engine:

```
Audit → Decision Engine → Risk Engine → Action Engine → Verification → Logging → GitHub (только если не исправлено)
```

Подробнее в [`ARCHITECTURE.md`](ARCHITECTURE.md) и [`AI/Decision/AI_DECISION_ENGINE.md`](AI/Decision/AI_DECISION_ENGINE.md).

## Быстрый старт

```bash
python3 Scripts/run_laos.py
```

## Структура

| Директория | Назначение |
|------------|------------|
| `AI/` | Исполнительная система: Decision Engine, движки, модели. |
| `Auditors/` | Модули аудита: SEO, структура, изображения, производительность, безопасность, WordPress. |
| `Framework/` | Правила, роли, чек-листы. |
| `Policies/` | Severity, rollback, framework reference. |
| `Registry/` | Реестр правил. |
| `Scripts/` | Entrypoints. |
| `Logs/` | Логи выполнения. |
| `Knowledge/` | База знаний о компании. |

## Ключевые принципы

1. **Безопасность превыше всего.** P0 и P1 не исправляются автоматически.
2. **Confidence < 0.70** → autofix запрещён.
3. **Framework reference** обязателен. Если правила нет — создаётся Issue «Framework Improvement».
4. **Любое изменение обосновано.** Ответ на «Что конкретно станет лучше?» обязателен.
5. **Verification после каждого действия.** Если не прошёл — rollback.
6. **GitHub Issue** — только как fallback, когда автоматика не справилась.

## Зоны ответственности

- **Зелёная** — агент действует автоматически (P2/P3 с высоким confidence).
- **Жёлтая** — агент предлагает варианты (P1, P2 с низким confidence).
- **Красная** — только после подтверждения владельца (P0, P1).

## Статус

Версия 1.0.0 — MVP с аудиторами, Decision Engine и логированием. Автоматическое применение изменений к сайту в этом релизе не производится: Action Engine возвращает план действий, Verification Engine проверяет текущее состояние.

## Лицензия

Внутренний проект laser178.ru.
