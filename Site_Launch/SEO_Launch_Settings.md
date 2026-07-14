# SEO-настройки для запуска laser178.ru

## Цель

Убрать технические SEO-риски и настроить индексацию до запуска.

## 1. Sitemap

### Проблема

`page-sitemap.xml` содержит только главную страницу. Остальные 17 страниц в sitemap не попадают.

### Решение

1. **Yoast SEO → Настройки → Карта сайта → Типы контента**.
2. Убедиться, что **Страницы** включены в sitemap.
3. Если отключены — включить.
4. Очистить кэш.
5. Проверить: `https://laser178.ru/page-sitemap.xml` должен содержать URL всех публичных страниц.

### Рекомендуемый список страниц в sitemap

- https://laser178.ru/
- https://laser178.ru/about/
- https://laser178.ru/services/
- https://laser178.ru/works/
- https://laser178.ru/before-after/
- https://laser178.ru/pricing/
- https://laser178.ru/contacts/
- https://laser178.ru/booking/
- https://laser178.ru/blog/ (или /bortovoj-zhurnal/)
- https://laser178.ru/risk-test/
- https://laser178.ru/sledit-za-modelju/
- https://laser178.ru/privacy-policy/
- https://laser178.ru/guarantee/

## 2. Дубли страниц

### Проблема

В WordPress существуют 4 пары дублей, обе версии доступны и возвращают 200:

| Основная | Дубль | Действие |
|----------|-------|----------|
| `/blog/` | `/bortovoj-zhurnal/` | 301 на `/blog/` |
| `/before-after/` | `/galereja-do-posle/` | 301 на `/before-after/` |
| `/sledit-za-modelju/` | `/follow-model/` | 301 на `/sledit-za-modelju/` |
| `/risk-test/` | `/proverit-ugrozu/` | 301 на `/risk-test/` |

### Решение

Добавить 301 редиректы. Варианты:

#### Вариант A — плагин Redirection

1. Установить **Redirection**.
2. Добавить редиректы:

| Source URL | Target URL |
|------------|------------|
| `/bortovoj-zhurnal/` | `/blog/` |
| `/galereja-do-posle/` | `/before-after/` |
| `/follow-model/` | `/sledit-za-modelju/` |
| `/proverit-ugrozu/` | `/risk-test/` |

3. Сохранить.

#### Вариант B — .htaccess

```apache
Redirect 301 /bortovoj-zhurnal/ /blog/
Redirect 301 /galereja-do-posle/ /before-after/
Redirect 301 /follow-model/ /sledit-za-modelju/
Redirect 301 /proverit-ugrozu/ /risk-test/
```

После настройки редиректов удалить дублирующиеся страницы (или перевести в черновики).

## 3. Meta title и description

### Проблема

Нет подтверждённых данных, что все страницы имеют оптимальные title/description. В `Page_Content_*.md` уже подготовлены варианты.

### Рекомендации по title

| Страница | Title |
|----------|-------|
| Главная | Лазерная очистка и антикор авто в СПб — гарантия до 5 лет \| Лазер Антикор |
| О нас | О нас — Лазер Антикор в Санкт-Петербурге \| Лазерная очистка и антикор |
| Услуги | Услуги — Лазерная очистка и антикор в СПб \| Цены \| Лазер Антикор |
| Наши работы | Наши работы — до и после \| Лазерная очистка и антикор в СПб |
| Контакты | Контакты — Лазер Антикор в Санкт-Петербурге \| Адрес и телефон |
| Блог | Бортовой журнал — Лазер Антикор \| Полезное об авто в СПб |

### Рекомендации по description

- Длина 120–160 символов.
- Включить «Санкт-Петербург», «СПб» или «Санкт-Петербург».
- Указать ключевое преимущество (гарантия, цены, без абразива).

## 4. Микроразметка

### Рекомендуемые типы Schema.org

- **AutoRepair** — для страницы контактов и главной (основная организация).
- **LocalBusiness** — альтернатива AutoRepair.
- **BreadcrumbList** — хлебные крошки.
- **Service** — для страницы Услуги (можно на каждую услугу).
- **Article** — для постов блога.
- **FAQPage** — для страниц с FAQ.

### Пример JSON-LD для главной (организация)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "AutoRepair",
  "name": "Лазер Антикор",
  "url": "https://laser178.ru/",
  "logo": "https://laser178.ru/wp-content/uploads/logo.png",
  "telephone": "+79810971505",
  "email": "info@laser178.ru",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Санкт-Петербург",
    "streetAddress": "ул. Грузинская, 3 корп. 1П",
    "addressCountry": "RU"
  },
  "openingHours": ["Mo-Fr 10:00-19:00", "Sa 10:00-15:00"],
  "priceRange": "₽₽"
}
</script>
```

## 5. Robots.txt

### Рекомендуемый robots.txt

```text
User-agent: *
Disallow: /wp-admin/
Disallow: /wp-includes/
Disallow: /wp-content/plugins/
Disallow: /wp-content/themes/
Disallow: /search/
Allow: /wp-content/uploads/

Sitemap: https://laser178.ru/sitemap_index.xml
```

## 6. HTTPS и www

### Проверить

- Сайт должен открываться только по `https://laser178.ru/`.
- Версия `http://` должна редиректить на `https://`.
- Версия `www` должна редиректить на без `www` (или наоборот — главное, единообразие).

### Проверка командами

```bash
curl -I http://laser178.ru/
curl -I https://www.laser178.ru/
```

Ожидаемый результат: `HTTP/2 301` с `Location: https://laser178.ru/`.

## 7. Search Console и Яндекс.Вебмастер

### До запуска

1. Добавить сайт в [Google Search Console](https://search.google.com/search-console).
2. Добавить сайт в [Яндекс.Вебмастер](https://webmaster.yandex.ru).
3. Подтвердить права через HTML-файл или DNS-запись.
4. Загрузить sitemap: `https://laser178.ru/sitemap_index.xml`.
5. Проверить индексацию через `site:laser178.ru`.

### После запуска

1. Проверить отчёт «Покрытие» в Search Console.
2. Проверить ошибки сканирования в Вебмастере.
3. Проверить Core Web Vitals.

## 8. Open Graph

### Рекомендуемые теги для каждой страницы

```html
<meta property="og:title" content="...">
<meta property="og:description" content="...">
<meta property="og:type" content="website">
<meta property="og:url" content="https://laser178.ru/...">
<meta property="og:image" content="https://laser178.ru/wp-content/uploads/og-image.jpg">
<meta property="og:locale" content="ru_RU">
```

Yoast SEO генерирует большинство этих тегов автоматически. Нужно задать изображение по умолчанию в настройках Yoast → Социальные сети.

## 9. Контрольный чек-лист SEO

- [ ] Все публичные страницы в sitemap.
- [ ] Дубли устранены через 301.
- [ ] Title и description уникальны для каждой страницы.
- [ ] H1 уникальны и не повторяются.
- [ ] Микроразметка LocalBusiness/AutoRepair на главной и контактах.
- [ ] Robots.txt корректный.
- [ ] HTTPS и редиректы настроены.
- [ ] Search Console и Вебмастер подключены.
- [ ] Open Graph настроен.
- [ ] Все изображения имеют alt-теги.

---

**Приоритет для запуска:** настроить sitemap (P1-2) и убрать дубли (P1-4) — это решается в админке за 10–15 минут.
