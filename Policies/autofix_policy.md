# Autofix Policy

## Версия

1.0.0

## Определение

Autofix — автоматическое изменение сайта без участия человека.

## Когда autofix разрешён

1. Severity P2 или P3.
2. Confidence ≥ 0.70.
3. Capability разрешена.
4. Environment не production, либо production override активирован.
5. Dry Run прошёл успешно.
6. Backup выполнен и проверен.
7. Rollback возможен.
8. Framework reference существует.
9. Требуемый approval получен (если applicable).

## Когда autofix запрещён

| Условие | Действие |
|---------|----------|
| Severity P0 или P1 | autofix запрещён, создаётся approval. |
| Confidence < 0.70 | autofix запрещён, создаётся issue или approval. |
| Capability отсутствует | запрещено, создаётся issue «Framework Improvement». |
| Environment = production без override | запрещено, создаётся approval. |
| Dry Run не пройден | запрещено, лог. |
| Backup не выполнен | запрещено, лог. |
| Rollback невозможен | запрещено, approval. |
| Framework reference отсутствует | запрещено, issue «Framework Improvement». |
| Действие изменяет >N страниц | требуется approval, autofix запрещён. |

## Разрешённые autofix в MVP

| Тип | Описание |
|-----|----------|
| edit_title | Изменение title на одной странице. |
| edit_description | Изменение meta description. |
| normalize_h1 | Удаление/объединение дублирующих H1. |
| add_canonical | Добавление canonical link. |
| add_alt | Добавление alt к изображению. |
| remove_generator_meta | Удаление meta generator WordPress. |

## Любое autofix независимо от severity

- Проходит через Verification Engine.
- Если verification не прошёл — rollback.
- Логируется.
