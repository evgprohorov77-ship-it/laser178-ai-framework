# Governance: Permissions

## Статус

- **Действует с:** LAOS-005
- **Автор:** Owner
- **Цель:** зафиксировать, какие действия разрешены для каждой роли и в каких областях.

## Области системы

1. **Owner Portal** — файлы в `Owner/`, редактируемые владельцем.
2. **Knowledge** — файлы в `Knowledge/`, обновляемые через синхронизацию из Owner Portal.
3. **Governance** — файлы в `Governance/`, RFC, политики.
4. **Content** — статьи, FAQ, описания, черновики.
5. **Production** — сайт laser178.ru, хостинг, FTP, WordPress.
6. **Security** — секреты, credentials, токены, ключи.
7. **Audit** — логи, отчёты, проверки.

## Матрица прав

| Область | Owner | Hermes | Operator | Auditor |
|---------|-------|--------|----------|---------|
| Owner Portal | чтение/запись | чтение | чтение | чтение |
| Knowledge | чтение/запись* | чтение/запись* | чтение | чтение |
| Governance | чтение/запись | чтение/запись** | чтение | чтение |
| Content | чтение/запись | чтение/запись** | чтение/запись** | чтение |
| Production | чтение/запись*** | чтение | чтение/запись*** | чтение |
| Security | полный доступ | нет доступа | ограниченный | чтение |
| Audit | чтение/запись | чтение/запись | чтение/запись | чтение |

\* Hermes обновляет Knowledge только через синхронизацию из Owner Portal, не напрямую.  
\*\* Hermes и Operator могут предлагать изменения, но не публиковать без owner approval.  
\*\*\* Production изменения выполняет Operator после owner approval; Owner может выполнить сам.

## Подробные разрешения

### Owner Portal

- Owner может редактировать любые файлы в `Owner/`.
- Hermes может читать `Owner/` для синхронизации.
- Operator и Auditor имеют только чтение.

### Knowledge

- Owner может редактировать напрямую в исключительных случаях.
- Hermes обновляет Knowledge через `Scripts/sync_owner_to_knowledge.py` после валидации.
- Никто не может менять Knowledge без валидации.

### Governance

- Owner может изменять политики в любой момент.
- Hermes может предлагать изменения через RFC.
- Все изменения фиксируются в Changelog.

### Content

- Hermes генерирует черновики в `Content/Drafts/` или `Verification/`.
- Owner review и approval обязателен перед публикацией.
- Operator публикует только после owner approval.

### Production

- Hermes не подключается к production напрямую.
- Operator выполняет изменения через инструменты, одобренные Owner (FTP, GitHub Actions, тестовый стенд).
- Owner может сам выполнить изменение, но обязан зафиксировать его в Changelog.

### Security

- Hermes не хранит и не получает пароли, API-ключи, токены.
- Operator может использовать credentials только из одобренного хранилища (например, 1Password, Bitwarden, pass) и только с owner approval.

### Audit

- Все действия пишутся в `Audit/` с датой, ролью, действием и результатом.
- Auditor не может изменять логи.

## Запрещённые действия

- Hermes не может публиковать в Production без approval.
- Hermes не может менять цены, гарантии, юридические условия без owner approval.
- Hermes не может создавать новые Engines, Adapters или архитектурные слои.
- Operator не может давать final approval.
- Никто не может удалять старые `.md` из `Knowledge/Company/` без owner approval и архивации.

## Примечание

Права Owner являются надмножеством всех остальных прав. Owner может делегировать часть прав Operator, но это должно быть зафиксировано в `Governance/roles.md` и `Governance/approval_matrix.md`.
