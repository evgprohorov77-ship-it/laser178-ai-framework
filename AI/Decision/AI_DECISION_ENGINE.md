# AI Decision Engine

## Версия

1.0.0

## Автор

Hermes LAOS

## Цель

Описать, как ИИ-агент принимает решения об изменениях на сайте `laser178.ru`. Документ является обязательным к применению. Любое действие агента должно проходить через Decision Engine.

## Принципы

1. **Безопасность превыше всего.** Не допускаем поломки работающего сайта.
2. **Изменение обосновано.** Каждое действие отвечает на вопрос: «Что конкретно станет лучше?»
3. **Прозрачность.** Все решения логируются и связываются с Framework Reference.
4. **Контроль владельца.** P0 и P1 — владелец всегда в курсе.
5. **Откат.** Если автоматическое исправление невозможно откатить — оно запрещено.

## Поток принятия решений

### 1. Поступление Finding

Аудитор возвращает объект `Finding`.

Обязательные поля:

- `rule_id`
- `title`
- `description`
- `url`
- `severity`
- `confidence`
- `autofix`
- `requires_confirmation`
- `rollback_required`
- `framework_reference`
- `category`
- `timestamp`
- `agent_version`

### 2. Проверка Framework Reference

Если `framework_reference` пуст или отсутствует:

- Decision Engine создаёт Issue «Framework Improvement: missing rule for {rule_id}».
- Finding отправляется в ручную обработку.
- Autofix запрещён.

### 3. Проверка Confidence

- `confidence < 0.70` → autofix запрещён.
- `confidence < 0.70` + P3 → можно отклонить как ложное срабатывание, если есть обоснование.
- `confidence < 0.70` + P2/P1/P0 → создаётся Issue для ручной проверки.

### 4. Классификация Severity

#### P0 — Критическая

- Сайт не работает или может перестать работать.
- Потеря данных, утечка, взлом.
- **Решение:** создать Issue, немедленно уведомить владельца, autofix запрещён.

#### P1 — Высокая

- Безопасность, SEO-ущерб, потенциальная потеря данных.
- **Решение:** запросить подтверждение владельца. Autofix запрещён без согласия.

#### P2 — Средняя

- SEO, структура, скорость, UX.
- **Решение:** autofix разрешён при confidence ≥ 0.70 и наличии rollback.

#### P3 — Низкая

- Рекомендации, улучшения, орфография, ALT, описание.
- **Решение:** autofix разрешён для очевидных правок (опечатки, missing ALT). Если изменение не удаётся проверить — создать Issue.

### 5. Проверка Autofix

Autofix разрешён только если:

- `severity` ∈ {P2, P3}
- `confidence` ≥ 0.70
- `framework_reference` существует
- `rollback_required` имеет рабочий rollback-план
- Action Engine поддерживает тип действия

### 6. Проверка Rollback

Если `rollback_required == true`:

- перед действием создаётся резервная копия;
- после действия Verification Engine проверяет результат;
- если verify не пройден — выполняется rollback.

### 7. Действие

Decision Engine возвращает `Decision`:

```json
{
  "action": "autofix",
  "reason": "P2, confidence 0.98, rollback available",
  "assigned_engine": "action_engine",
  "requires_rollback": true,
  "owner_prompt": null
}
```

Доступные значения `action`:

- `autofix` — исправить автоматически.
- `ask` — запросить подтверждение владельца.
- `issue` — создать GitHub Issue.
- `reject` — отклонить как ложное срабатывание.
- `framework_improvement` — создать Issue на улучшение Framework.

### 8. Verification

После autofix:

- страница открывается (HTTP 200);
- нет новых ошибок;
- нет новых H1 (если проблема была H1);
- проблема действительно устранена;
- не появились новые предупреждения.

Если verify не пройден — rollback и Issue.

### 9. Logging

Каждый шаг записывается в `Logs/YYYY-MM-DD/`, в формате JSON Lines.

### 10. GitHub Issue

Issue создаётся только если:

- autofix невозможен;
- владелец не подтвердил действие;
- Decision Engine отклонил autofix;
- rollback не удался.

## Примеры решений

### Пример 1: Duplicate H1

```json
{
  "rule_id": "SEO-004",
  "title": "Duplicate H1 on homepage",
  "severity": "P2",
  "confidence": 0.98,
  "autofix": true,
  "requires_confirmation": false,
  "rollback_required": false,
  "framework_reference": "SEO-001 §4.3"
}
```

**Решение:** autofix (убрать лишний H1 через CSS или изменить шаблон страницы).

### Пример 2: Title > 60 символов

```json
{
  "rule_id": "SEO-002",
  "title": "Title too long",
  "severity": "P2",
  "confidence": 1.0,
  "autofix": true,
  "requires_confirmation": false,
  "rollback_required": false,
  "framework_reference": "SEO-001 §2.1"
}
```

**Решение:** autofix (сформировать новый title в рамках правил SEO-001).

### Пример 3: Подозрение на взлом

```json
{
  "rule_id": "SEC-001",
  "title": "Unexpected admin user created",
  "severity": "P0",
  "confidence": 0.85,
  "autofix": false,
  "requires_confirmation": true,
  "rollback_required": false,
  "framework_reference": "SEC-001 §1.1"
}
```

**Решение:** Issue + немедленное уведомление владельца. Autofix запрещён.

## Запрещённые действия

1. Изменять тему WordPress.
2. Удалять плагины.
3. Изменять URL существующих страниц.
4. Менять DNS/домен.
5. Сбрасывать кэш, если нет резервной копии.
6. Изменять права пользователей без подтверждения.
7. Автоматически исправлять P0/P1.
8. Исправлять любое P2/P3, если нет ответа на «что станет лучше».

## Обязанности агента

1. Перед действием: проверить rollback.
2. Во время действия: создавать минимальные изменения.
3. После действия: провести verification.
4. При ошибке: откатиться и сообщить.
5. Всегда: логировать.

## Связанные документы

- `AI/Decision/README.md`
- `AI/Engines/risk_engine.py`
- `AI/Engines/action_engine.py`
- `AI/Engines/verification_engine.py`
- `Policies/rollback_policy.md`
- `Framework/quality-checklist.md`
- `Framework/zones.md`
