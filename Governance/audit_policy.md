# Governance: Audit Policy

## Статус

- **Действует с:** LAOS-005
- **Автор:** Owner
- **Цель:** определить, что фиксируется, кто проверяет и как хранятся аудиторские записи.

## Что фиксируется

1. **Все изменения в Knowledge.**
   - Кто изменял (Owner, Hermes, Operator).
   - Какой файл.
   - Дата и время.
   - Причина (RFC, owner request, verification).

2. **Все изменения в Owner Portal.**
   - Редактирование `Owner/*.yaml`.
   - Синхронизация с Knowledge.
   - Результаты валидации.

3. **Все изменения в Governance.**
   - Изменения ролей, прав, матрицы, процессов.
   - RFC и их статусы.

4. **Все попытки доступа к Production.**
   - Дата, роль, действие, результат.
   - Даже если действие не было выполнено.

5. **Все инциденты.**
   - См. `Governance/incident_response.md`.

6. **Все проверки и валидации.**
   - Результаты `validate_knowledge.py`.
   - Результаты `check_content.py`.
   - Любые другие проверки.

## Формат аудиторской записи

Каждая запись — отдельный файл в `Audit/`:

```markdown
# Audit Record: AUDIT-YYYY-MM-DD-NNN

- **Date:** YYYY-MM-DD HH:MM
- **Actor:** Owner / Hermes / Operator
- **Action:** ...
- **Target:** файл или система
- **Reason:** RFC-NNNN / owner request / verification
- **Result:** success / failure / partial
- **Evidence:** ссылка на commit, лог, скриншот
- **Notes:** ...
```

## Хранение

```
Audit/
├── validation/
├── incidents/
├── access/
├── changes/
└── README.md
```

- Файлы не удаляются.
- Можно дополнять существующие записи, но не изменять их.
- Хранятся в Git, поэтому есть полная история.

## Кто проверяет

- **Owner:** может проверить любую запись в любой момент.
- **Auditor:** читает записи и готовит отчёты.
- **Hermes:** помогает собирать и форматировать записи, но не удаляет их.

## Периодичность аудита

| Тип | Частота | Кто |
|-----|---------|-----|
| Проверка валидаций | После каждого изменения | Hermes / Operator |
| Review инцидентов | В рамках incident response | Owner / Operator |
| Compliance review | Раз в месяц | Owner / Auditor |
| Полный аудит Governance | Раз в квартал | Owner / Auditor |

## Публичность

- Audit-файлы не публикуются на сайте.
- Они могут содержать sensitive data (REDACTED, секреты).
- Доступ только для Owner, Operator и Auditor.

## Нарушения

Если обнаружено несоответствие Governance:
1. Зафиксировать в `Audit/incidents/`.
2. Уведомить Owner.
3. Подготовить RFC с исправлением.
4. Owner approval → исправление → verification → release.

## Примечание

Audit Policy — часть Governance. Изменения только через owner approval и RFC, если это меняет существенные положения.
