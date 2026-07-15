# Подключение laser178.ru к Яндекс.Вебмастеру и Google Search Console

## Подготовка

- Для Яндекс.Вебмастера нужен Яндекс-аккаунт.
- Для Google Search Console нужен Google-аккаунт.
- Способ подтверждения: **HTML-файл** (самый простой) или **мета-тег** в `<head>`.

Для WordPress + Hello Elementor + Yoast SEO рекомендуем **мета-тег** — он не требует загрузки файлов в корень.

---

## 1. Яндекс.Вебмастер

1. Открыть https://webmaster.yandex.ru/
2. Нажать **«Добавить сайт»**.
3. Ввести `https://laser178.ru/` → **Добавить**.
4. Выбрать способ подтверждения **«Мета-тег»**.
5. Скопировать строку вида:
   ```html
   <meta name="yandex-verification" content="XXXXXXXXXXXXXXXX" />
   ```
6. Войти в админку WordPress: `https://laser178.ru/wp-admin/`.
7. Перейти **Yoast SEO → Общие → Инструменты → Редактор файлов**.
8. Вставить мета-тег в поле **Заголовок сайта (header.php)** между `<head>` и `</head>`.
   Или:
   - **Elementor → Custom Code** → добавить новый код с расположением `<head>` и вставить мета-тег.
9. Сохранить.
10. Вернуться в Вебмастер и нажать **«Проверить»**.

---

## 2. Google Search Console

1. Открыть https://search.google.com/search-console
2. Нажать **«Добавить ресурс»**.
3. Выбрать **«Ресурс с префиксом в URL»**.
4. Ввести `https://laser178.ru/` → **Продолжить**.
5. Выбрать способ подтверждения **«HTML-тег»**.
6. Скопировать строку вида:
   ```html
   <meta name="google-site-verification" content="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" />
   ```
7. Вставить в тот же `<head>`, где был мета-тег Яндекса.
8. Сохранить.
9. Вернуться в Search Console и нажать **«Подтвердить»**.

---

## 3. Альтернатива: подтверждение через HTML-файл

Если мета-тег не сработает:

1. Скачать предложенный файл (например, `googleXXXXXXXXXXXXXXXX.html` или `yandex_XXXXXXXXXXXXXXXX.html`).
2. Загрузить в корень сайта `/public_html/` через FTP или файловый менеджер Beget.
3. Проверить, что файл открывается по адресу:
   - `https://laser178.ru/googleXXXXXXXXXXXXXXXX.html`
   - `https://laser178.ru/yandex_XXXXXXXXXXXXXXXX.html`
4. Нажать **«Подтвердить»** в сервисе.

---

## 4. После подтверждения

### Яндекс.Вебмастер:

- Перейти в **Индексирование → Файлы Sitemap**.
- Добавить: `https://laser178.ru/sitemap_index.xml`
- Проверить, что в разделе **Диагностика** нет критических ошибок.

### Google Search Console:

- Перейти в **Sitemaps** (в левом меню).
- Добавить: `https://laser178.ru/sitemap_index.xml`
- Дождаться статуса «Успешно».
- Через 2–7 дней проверить раздел **Страницы** — сколько страниц в индексе.

---

## 5. Проверка, что мета-теги на месте

```bash
curl -s https://laser178.ru/ | grep -iE "yandex-verification|google-site-verification"
```

Если выводит строки с мета-тегами — подтверждение пройдёт.

---

*Инструкция подготовлена 2026-07-15. После получения кодов подтверждения можно внедрить через FTP или Elementor Custom Code за 5 минут.*
