# Dry Run Policy

## Версия

1.0.0

## Определение

Dry Run — имитация изменения без реального применения к сайту.

## Правило

Перед **ЛЮБЫМ** изменением LAOS обязан выполнить Dry Run и показать результат владельцу.

## Что показывает Dry Run

1. **Что изменится.**
   - title → new title.
   - description → new description.
   - H1 → new H1.
   - canonical → new canonical.
2. **Какие страницы.**
   - URL целевой страницы.
   - Затронуты ли связанные страницы.
3. **Какие файлы.**
   - БД (таблица, запись).
   - Файлы темы/плагина.
   - robots.txt, .htaccess и т.д.
4. **Какие риски.**
   - Severity.
   - Confidence.
   - Возможные побочные эффекты.
5. **Какие rollback.**
   - Backup UUID.
   - Способ отката.
   - Время отката.

## Порядок

```
Request → Dry Run → Review → Owner Approval → Backup → Action → Verification
```

## Без Dry Run — нет действия

Authorization Engine отказывает в любом действии, если Dry Run не выполнен.

## Формат отчёта

```json
{
  "dry_run_uuid": "...",
  "finding_id": "...",
  "target_url": "...",
  "proposed_changes": [...],
  "affected_pages": [...],
  "affected_files": [...],
  "risks": [...],
  "rollback_plan": {...},
  "status": "ready_for_review"
}
```

## Разрешение на действие

Dry Run сам по себе не применяет изменения.  
Для применения требуется отдельный approval.
