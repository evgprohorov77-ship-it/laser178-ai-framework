# Governance: Change Management

## Статус

- **Действует с:** LAOS-005
- **Автор:** Owner
- **Цель:** установить единый процесс для любого изменения в системе.

## Процесс: от идеи до релиза

```
Идея / Запрос
      ↓
   RFC (Request for Change)
      ↓
   Review
      ↓
   Approval
      ↓
   Implementation
      ↓
   Verification
      ↓
   Release
      ↓
   Changelog
```

## 1. Идея / Запрос

- Источник: Owner, Hermes, Operator, GitHub Issue, Telegram, Email.
- Hermes преобразует идею в формальный RFC, если изменение затрагивает:
  - Knowledge (сущности, схема);
  - Governance (политики, роли, матрица);
  - Content (публикация статьи/FAQ);
  - Production (любое изменение сайта);
  - Security (доступы, секреты, политики);
  - Architecture (LAOS Core — запрещено без особого решения Owner).

## 2. RFC (Request for Change)

Каждый RFC содержит:
- **ID** (например, RFC-0007);
- **Название**;
- **Статус**: `draft`, `proposed`, `approved`, `rejected`, `implemented`, `closed`;
- **Автор**;
- **Обоснование** (зачем нужно изменение);
- **Описание изменения**;
- **Риски**;
- **Альтернативы**;
- **Кто утверждает** (см. `Governance/approval_matrix.md`);
- **Связанные файлы**;
- **План проверки**;
- **Changelog entry**.

RFC хранятся в `RFC/`.

## 3. Review

- Hermes проверяет RFC на соответствие Governance, схеме Knowledge и правам.
- Operator проверяет техническую осуществимость.
- Owner проверяет бизнес-целесообразность.
- Review может быть асинхронным (через Telegram/Email/GitHub).

## 4. Approval

- Owner даёт final approval.
- Для автоматических изменений (орфография, ALT) Hermes может дать формальное approval после проверки, если Owner заранее делегировал это.
- Без approval Implementation не начинается.

## 5. Implementation

- Hermes или Operator выполняет изменение в соответствии с RFC.
- Все изменения в код/данные — через Git.
- Production-изменения выполняются через approved инструменты (FTP, GitHub Actions, тестовый стенд).

## 6. Verification

- Запускаются валидаторы (`validate_knowledge.py`, `check_content.py`).
- Проверяется соответствие RFC.
- Для content — review сгенерированного текста.
- Для production — smoke test на тестовом стенде или вручную.

## 7. Release

- См. `Governance/release_policy.md`.
- Релиз фиксируется тегом и записью в Changelog.
- Major релизы (v1.x → v2.x) только через RFC.

## 8. Changelog

- Каждое изменение фиксируется в `Changelog/`.
- Запись содержит: дату, ID RFC, автор, что изменено, почему, статус verification.

## Исключения и hotfix

- **Critical incident** (сайт не работает, данные повреждены) может быть исправлен без полного RFC, но по pre-approved процедуре `Governance/incident_response.md`.
- После hotfix обязательно:
  - Owner уведомляется;
  - Фиксируется в Changelog;
  - Документируется в `Audit/`.

## Запреты

- Не создавать RFC для орфографических правок, если Owner заранее делегировал их AI.
- Не пропускать approval для production, цен, гарантий, юридических условий.
- Не изменять LAOS Core (Engines, Adapters) без отдельного решения Owner.
