# SOP: Резервное копирование плагинов

**Цель:** создать копию всех PHP/CSS/JS-файлов плагинов перед правкой, чтобы можно было откатиться.

**Зона:** зелёная (выполняется автоматически перед любой правкой).

## Шаги

1. Скачать текущий файл с FTP.
2. Сохранить в `Archive/YYYY-MM-DD/имя_файла` в репозитории.
3. Создать коммит с описанием: `backup: имя_файла перед правкой ISSUE-NN`.
4. Только после этого внести правку.

## Пример

```bash
# Локальная копия
mkdir -p /root/laser178-ai-framework/Archive/2026-07-12
cp /root/site-extract/wp-content/plugins/laser178-style.css \
   /root/laser178-ai-framework/Archive/2026-07-12/laser178-style.css

# Коммит
git add Archive/2026-07-12/laser178-style.css
git commit -m "backup: laser178-style.css before fix #1"
```

## Правило

Без backup правка не выполняется.
