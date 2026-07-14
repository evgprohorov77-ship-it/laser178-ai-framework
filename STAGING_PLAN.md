# STAGING_PLAN.md

## Версия

1.0.0

## Статус

На согласовании у владельца.

## Контекст

- **LAOS Foundation v1.0 считается завершённой.**
- **Разработка LAOS прекращена** до отдельного решения владельца.
- **Приоритет проекта — рост сайта `laser178.ru`.**
- Следующий шаг — подготовить безопасный **staging**.
- После staging — помочь владельцу завершить сайт.
- После запуска — перейти в режим сопровождения.
- **Запрещено:** подключать production, использовать production credentials, выполнять действия на production.

## Цель

Получить полную копию сайта `laser178.ru` на отдельной среде, на которой будут тестироваться все автоматические изменения до применения в production.

---

## 1. Как создать staging

### Вариант 1. Поддомен на текущем Beget-аккаунте (рекомендуемый)

**Шаги:**

1. Войти в панель управления Beget.
2. Создать новый поддомен: `staging.laser178.ru` (или `dev.laser178.ru`).
3. Создать новую директорию для staging: `/staging.laser178.ru/` или `/public_html/staging/`.
4. Создать отдельную базу данных MySQL (например, `laser178_staging`).
5. Создать отдельного FTP/SSH-пользователя с доступом только к директории staging.
6. Создать отдельного пользователя WordPress с ролью **Editor** (или **Administrator** с ограниченными capabilities, см. `Security/WordPress/permissions.yaml`).
7. Сгенерировать WordPress **Application Password** для staging.

**Плюсы:**
- Быстро и дёшево.
- Один хостинг, один счёт.
- Близкая к production конфигурация.

**Минусы:**
- Ресурсы shared hosting делятся между production и staging.
- Ошибка на staging потенциально может затронуть соседний аккаунт (маловероятно, но возможно).

### Вариант 2. Отдельный хостинг / сервер (VPS)

**Шаги:**

1. Заказать VPS (например, Beget Cloud, Timeweb, Selectel, Yandex Cloud).
2. Установить стек LAMP/LEMP (Apache/Nginx + MySQL/MariaDB + PHP 8.x).
3. Установить WordPress вручную или из бэкапа.
4. Настроить домен/поддомен, направленный на VPS.

**Плюсы:**
- Полная изоляция от production.
- Можно отключить когда не нужен.
- Возможность сохранить snapshot.

**Минусы:**
- Дополнительные затраты.
- Требует настройки окружения.
- Конфигурация может отличаться от production.

### Рекомендация

**Вариант 1** — поддомен на Beget. Это оптимальный баланс по стоимости, скорости и близости к production.

---

## 2. Какие данные копируются

### Обязательно копируем

1. **Файлы WordPress:**
   - `/wp-content/uploads/` — изображения, медиа.
   - `/wp-content/plugins/` — плагины (включая Elementor, Yoast и т.д.).
   - `/wp-content/themes/` — темы (Hello Elementor, дочерние темы, кастомные CSS).
   - `/wp-config.php` — конфигурация (с последующей адаптацией, см. раздел 4).
   - `.htaccess` — правила rewrite (если есть кастомные).

2. **База данных:**
   - Полный дамп MySQL production.
   - Все таблицы: `wp_posts`, `wp_postmeta`, `wp_options`, `wp_terms`, `wp_term_relationships`, `wp_term_taxonomy`, `wp_users`, `wp_usermeta`, `wp_yoast_seo_*` (если есть).

3. **Контент:**
   - Все страницы, посты, черновики.
   - Меню, виджеты, настройки темы, настройки Elementor.
   - SEO-настройки Yoast.
   - Комментарии (если есть).

### Рекомендуется скопировать

- История backup (если хранится локально).
- Логи ошибок (для диагностики).
- Кастомные файлы вне WordPress (если есть).

---

## 3. Какие данные не копируются

### Не копируем или заменяем

1. **Production credentials:**
   - Логины/пароли администраторов WordPress.
   - API-ключи, токены, reCAPTCHA keys.
   - Почтовые SMTP-настройки.
   - Ключи платёжных систем (если будут).

2. **Аналитика и трекинг:**
   - Google Analytics ID.
   - Яндекс.Метрика ID.
   - Facebook Pixel, VK Pixel и т.д.
   - Коды рекламных пикселей.

3. **Индексация:**
   - Sitemap ping-настройки поисковикам.
   - Robots.txt production-версии.
   - Open Graph / Twitter cards, указывающие на production URL.

4. **Данные пользователей:**
   - Клиентские заявки из форм (если хранятся в БД).
   - Персональные данные посетителей.
   - Комментарии с email-адресами (при необходимости анонимизировать).

5. **Кэш и временные файлы:**
   - `/wp-content/cache/`
   - `/wp-content/upgrade/`
   - `/wp-content/backup-db/`
   - Логи кэш-плагинов.

6. **Почта:**
   - Вся исходящая почта staging должна быть отключена или перехвачена (например, через плагин `WP Mail Logging` или MailHog).

### Рекомендация

После копирования обновить в `wp_options` все записи, содержащие `laser178.ru`, на staging URL.

---

## 4. Как заменить URL

### После импорта базы данных в staging

Выполнить SQL-запросы (заменить `staging.laser178.ru` на актуальный поддомен):

```sql
UPDATE wp_options SET option_value = 'https://staging.laser178.ru' WHERE option_name = 'home';
UPDATE wp_options SET option_value = 'https://staging.laser178.ru' WHERE option_name = 'siteurl';
UPDATE wp_posts SET guid = REPLACE(guid, 'https://laser178.ru', 'https://staging.laser178.ru');
UPDATE wp_posts SET post_content = REPLACE(post_content, 'https://laser178.ru', 'https://staging.laser178.ru');
UPDATE wp_postmeta SET meta_value = REPLACE(meta_value, 'https://laser178.ru', 'https://staging.laser178.ru');
UPDATE wp_options SET option_value = REPLACE(option_value, 'https://laser178.ru', 'https://staging.laser178.ru');
```

### Для Elementor

Elementor хранит сериализованные данные. Используйте WP-CLI или плагин:

```bash
wp search-replace 'https://laser178.ru' 'https://staging.laser178.ru' --all-tables --allow-root
```

**Рекомендуется:** использовать плагин `Better Search Replace` с опцией «Run as dry run» сначала.

### Важно

- Перед заменой сделать backup базы данных.
- Не заменять внутри путей `/wp-content/` — это не URL сайта, а путь к файлам.
- Проверить, что в `wp-config.php` не захардкожен `WP_HOME` или `WP_SITEURL` — если да, обновить.

---

## 5. Как отключить индексацию

### 1. WordPress → Настройки → Чтение

- Установить галочку **«Попросить поисковые системы не индексировать сайт»**.
- Это добавляет `<meta name="robots" content="noindex, nofollow">` на все страницы.

### 2. Файл `robots.txt` staging

Создать/обновить `robots.txt` в корне staging:

```
User-agent: *
Disallow: /
```

### 3. HTTP-заголовок `X-Robots-Tag`

Если используется Nginx или Apache, добавить заголовок:

**Nginx:**
```nginx
add_header X-Robots-Tag "noindex, nofollow" always;
```

**Apache (.htaccess):**
```apache
Header set X-Robots-Tag "noindex, nofollow"
```

### 4. Удалить sitemap из поиска

- Убедиться, что `sitemap.xml` не отправлен в Google Search Console / Яндекс.Вебмастер для staging.
- Можно оставить sitemap для внутренней проверки, но добавить `X-Robots-Tag` на него.

### 5. Парольная защита (см. раздел 6)

Если стоит HTTP Basic Auth, поисковики не проиндексируют сайт даже без `noindex`.

---

## 6. Как защитить staging паролем

### Вариант 1. HTTP Basic Auth через панель Beget (рекомендуемый)

1. В панели Beget найти раздел «Защита директории паролем» или «Пароли на директории».
2. Выбрать директорию staging.
3. Создать пользователя `staging` с сильным паролем.
4. Сохранить настройки.

### Вариант 2. .htaccess + .htpasswd

В корне staging создать `.htaccess`:

```apache
AuthType Basic
AuthName "Staging Area"
AuthUserFile /path/to/staging/.htpasswd
Require valid-user
```

Создать `.htpasswd`:

```bash
htpasswd -cb /path/to/staging/.htpasswd staging_user STRONG_PASSWORD
```

### Вариант 3. Плагин WordPress

Установить плагин `Password Protected` или `Staging Site Password Protection`.

**Минусы:** плагин может конфликтовать с кэшем или Elementor.

### Рекомендация

**Вариант 1** — через панель Beget. Это надёжно, не зависит от WordPress и не ломается при обновлении плагинов.

---

## 7. Как синхронизировать production и staging

### Принцип

**Staging должен быть копией production, но не наоборот.**

### Регулярная синхронизация (перед важными тестами)

1. Сделать бэкап production:
   - База данных через Beget или плагин (UpdraftPlus, All-in-One WP Migration).
   - Файлы через FTP или файл-менеджер.
2. Перенести бэкап на staging.
3. Восстановить на staging.
4. Заменить URL (см. раздел 4).
5. Отключить индексацию (см. раздел 5).
6. Включить парольную защиту (см. раздел 6).
7. Очистить кэш staging.
8. Проверить, что staging открывается по `https://staging.laser178.ru`.

### Автоматизация (post-launch)

После запуска сайта можно настроить регулярную синхронизацию:
- Раз в неделю (перед плановыми обновлениями).
- Перед каждым крупным изменением.
- Вручную перед важными тестами.

**Важно:** staging никогда не должен синхронизироваться обратно в production.

### Рекомендуемый инструмент

- `Duplicator Pro` или `All-in-One WP Migration` для WordPress.
- WP-CLI для продвинутой автоматизации (если есть SSH на Beget).
- Ручное копирование через панель Beget, если автоматизация недоступна.

---

## 8. Как откатывать staging

### Откат к предыдущей версии staging

1. **Если есть snapshot/бэкап Beget:**
   - В панели Beget выбрать точку восстановления.
   - Восстановить файлы и/или базу данных.

2. **Если есть ручной бэкап:**
   - Удалить текущие файлы staging.
   - Распаковать архив бэкапа.
   - Импортировать дамп базы данных.
   - Провести замену URL (см. раздел 4).

3. **Если staging «сломался» после теста:**
   - Не пытаться чинить — удалить и пересоздать из последнего production-бэкапа.
   - Это быстрее и безопаснее.

### Рекомендация

Создать правило: **«Staging — расходный. Если что-то пошло не так — пересоздаём из production backup»**.

---

## Рекомендуемый порядок действий для владельца

1. Создать поддомен `staging.laser178.ru` в Beget.
2. Создать отдельную базу данных и FTP-пользователя.
3. Сделать бэкап production (файлы + БД).
4. Перенести бэкап на staging.
5. Восстановить на staging.
6. Заменить URL на `staging.laser178.ru`.
7. Отключить индексацию (robots + WP-настройка).
8. Включить HTTP Basic Auth через Beget.
9. Проверить доступность staging по паролю.
10. Предоставить Hermes URL staging и credentials (Application Password) для тестов WordPress Adapter.

После этого — можно проводить тестирование автоматических изменений на staging без риска для production.

---

## Статус

**Ожидает подтверждения владельца.**

