import requests, re, json, os
from urllib.parse import urljoin, urlparse

base = 'https://laser178.ru/'
headers = {'Cookie': 'beget=begetok'}

r = requests.get(base, headers=headers, timeout=30)
r.raise_for_status()
html = r.text

issues = []

# 1. Title length
title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
title = title_match.group(1) if title_match else ''
if title and len(title) > 60:
    issues.append({
        'title': '[SEO] Title главной страницы длиннее 60 символов',
        'body': f"""## URL\n{base}\n\n## Что не так\nTitle главной страницы длиннее 60 символов и может обрезаться в поисковой выдаче.\n\n**Текущий title:** `{title}`  \n**Длина:** {len(title)} символов\n\n## Ожидаемый результат\nTitle не длиннее 60 символов, содержит ключевой запрос и бренд.\n\n## Приоритет\n2 — важно\n\n## Селектор\ntitle""",
        'labels': ['content']
    })

# 2. Description length
desc_match = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)', html, re.IGNORECASE)
if not desc_match:
    desc_match = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']description["\']', html, re.IGNORECASE)
desc = desc_match.group(1) if desc_match else ''
if desc and len(desc) > 160:
    issues.append({
        'title': '[SEO] Description главной страницы длиннее 160 символов',
        'body': f"""## URL\n{base}\n\n## Что не так\nMeta description главной страницы длиннее 160 символов и может обрезаться в поисковой выдаче.\n\n**Текущий description:** `{desc}`  \n**Длина:** {len(desc)} символов\n\n## Ожидаемый результат\nDescription не длиннее 160 символов, содержит ключевой запрос, призыв к действию и регион.\n\n## Приоритет\n2 — важно""",
        'labels': ['content']
    })

# 3. Images without alt
imgs = re.findall(r'<img[^>]*>', html, re.IGNORECASE)
no_alt = []
for img in imgs:
    src_match = re.search(r'src=["\']([^"\']+)["\']', img, re.IGNORECASE)
    if not src_match:
        continue
    src = src_match.group(1)
    if not re.search(r'alt=["\'][^"\']*["\']', img, re.IGNORECASE):
        no_alt.append(src)

if no_alt:
    issues.append({
        'title': '[SEO] Изображения без ALT на главной странице',
        'body': f"""## URL\n{base}\n\n## Что не так\nНа главной странице обнаружены изображения без атрибута `alt`.\n\n**Количество:** {len(no_alt)}\n\n**Примеры:**\n{chr(10).join(['- ' + (x[:80] + ('...' if len(x) > 80 else '')) for x in no_alt[:5]])}\n\n## Ожидаемый результат\nУ всех изображений заполнен атрибут `alt` с описанием и ключевыми словами.\n\n## Приоритет\n2 — важно""",
        'labels': ['content']
    })

# 4. H1 count
h1_count = len(re.findall(r'<h1[^>]*>', html, re.IGNORECASE))
if h1_count != 1:
    issues.append({
        'title': '[SEO] На главной странице больше одного H1',
        'body': f"""## URL\n{base}\n\n## Что не так\nНа главной странице обнаружено {h1_count} тегов H1.\n\n## Ожидаемый результат\nРовно один H1 на странице.\n\n## Приоритет\n2 — важно""",
        'labels': ['content']
    })

# 5. robots.txt sitemap
robots = requests.get(urljoin(base, 'robots.txt'), headers=headers, timeout=15).text
if 'sitemap' not in robots.lower():
    issues.append({
        'title': '[SEO] В robots.txt не указан Sitemap',
        'body': f"""## URL\n{base}robots.txt\n\n## Что не так\nВ файле robots.txt не указана директива `Sitemap`.\n\n## Ожидаемый результат\nДобавить строку `Sitemap: {base}sitemap.xml` в robots.txt.\n\n## Приоритет\n2 — важно""",
        'labels': ['content']
    })

# 6. sitemap.xml availability
sitemap = requests.get(urljoin(base, 'sitemap.xml'), headers=headers, timeout=15)
if sitemap.status_code != 200:
    issues.append({
        'title': '[SEO] Sitemap.xml недоступен',
        'body': f"""## URL\n{base}sitemap.xml\n\n## Что не так\nSitemap.xml возвращает HTTP {sitemap.status_code}.\n\n## Ожидаемый результат\nSitemap.xml доступен и содержит актуальные URL страниц.\n\n## Приоритет\n2 — важно""",
        'labels': ['content']
    })

# 7. Check real internal links for 404 (exclude external, xmlrpc, wp-json, feeds, fonts)
links = re.findall(r'href=["\']([^"\']+)["\']', html, re.IGNORECASE)
pages_to_check = set()
for l in links:
    l = l.strip()
    if not l or l.startswith('#') or l.startswith('javascript:') or l.startswith('//'):
        continue
    if l.startswith('mailto:') or l.startswith('tel:') or l.startswith('whatsapp:'):
        continue
    if l.startswith('http'):
        parsed = urlparse(l)
        if parsed.netloc not in ['laser178.ru', 'www.laser178.ru']:
            continue
        path = parsed.path
    else:
        path = urlparse(l).path
        if path == '/' or not path:
            continue

    # Исключаем служебные
    if any(p in path for p in ['/xmlrpc.php', '/wp-json/', '/feed/', '/comments/', '/favicon']):
        continue

    pages_to_check.add(urljoin(base, l.split('#')[0]))

broken = []
for url in sorted(pages_to_check):
    try:
        rr = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        if rr.status_code >= 400:
            broken.append((url, rr.status_code))
    except Exception as e:
        broken.append((url, str(e)))

if broken:
    issues.append({
        'title': '[BUG] Битые внутренние ссылки на главной странице',
        'body': f"""## URL\n{base}\n\n## Что не так\nПри проверке внутренних ссылок с главной страницы обнаружены битые.\n\n{chr(10).join([f'- {url} → {status}' for url, status in broken])}\n\n## Ожидаемый результат\nВсе внутренние ссылки возвращают HTTP 200.\n\n## Приоритет\n1 — критично""",
        'labels': ['bug']
    })

# 8. Audit key pages: title, description, h1
pages_to_audit = {
    '/services/': 'Услуги',
    '/price/': 'Прайс',
    '/calculator/': 'Калькулятор',
    '/bortovoj-zhurnal/': 'Бортовой журнал',
}
for path, name in pages_to_audit.items():
    url = urljoin(base, path)
    try:
        rr = requests.get(url, headers=headers, timeout=15)
        if rr.status_code != 200:
            issues.append({
                'title': f'[BUG] Страница {name} недоступна',
                'body': f"""## URL\n{url}\n\n## Что не так\nСтраница `{name}` возвращает HTTP {rr.status_code}.\n\n## Ожидаемый результат\nСтраница доступна и возвращает HTTP 200.\n\n## Приоритет\n1 — критично""",
                'labels': ['bug']
            })
            continue
        page_html = rr.text
        page_title = re.search(r'<title>(.*?)</title>', page_html, re.I)
        title_text = page_title.group(1) if page_title else ''
        page_desc = re.search(r'<meta[^\u003e]+name=["\']description["\'][^\u003e]+content=["\']([^"\']+)', page_html, re.I)
        if not page_desc:
            page_desc = re.search(r'<meta[^\u003e]+content=["\']([^"\']+)["\'][^\u003e]+name=["\']description["\']', page_html, re.I)
        desc_text = page_desc.group(1) if page_desc else ''
        h1_count = len(re.findall(r'<h1[^\u003e]*>', page_html, re.I))

        if not title_text:
            issues.append({
                'title': f'[SEO] На странице {name} отсутствует title',
                'body': f"""## URL\n{url}\n\n## Что не так\nНа странице `{name}` не заполнен тег `title`.\n\n## Ожидаемый результат\nTitle заполнен, не длиннее 60 символов, содержит ключевой запрос и бренд.\n\n## Приоритет\n2 — важно""",
                'labels': ['content']
            })
        elif len(title_text) > 60:
            issues.append({
                'title': f'[SEO] Title на странице {name} длиннее 60 символов',
                'body': f"""## URL\n{url}\n\n## Что не так\nTitle на странице `{name}` длиннее 60 символов.\n\n**Текущий title:** `{title_text}`  \n**Длина:** {len(title_text)} символов\n\n## Ожидаемый результат\nTitle не длиннее 60 символов.\n\n## Приоритет\n2 — важно""",
                'labels': ['content']
            })

        if not desc_text:
            issues.append({
                'title': f'[SEO] На странице {name} отсутствует description',
                'body': f"""## URL\n{url}\n\n## Что не так\nНа странице `{name}` не заполнен meta description.\n\n## Ожидаемый результат\nDescription заполнен, не длиннее 160 символов, содержит ключевой запрос и регион.\n\n## Приоритет\n2 — важно""",
                'labels': ['content']
            })
        elif len(desc_text) > 160:
            issues.append({
                'title': f'[SEO] Description на странице {name} длиннее 160 символов',
                'body': f"""## URL\n{url}\n\n## Что не так\nDescription на странице `{name}` длиннее 160 символов.\n\n**Текущий description:** `{desc_text}`  \n**Длина:** {len(desc_text)} символов\n\n## Ожидаемый результат\nDescription не длиннее 160 символов.\n\n## Приоритет\n2 — важно""",
                'labels': ['content']
            })

        if h1_count != 1:
            issues.append({
                'title': f'[SEO] На странице {name} больше одного H1',
                'body': f"""## URL\n{url}\n\n## Что не так\nНа странице `{name}` обнаружено {h1_count} тегов H1.\n\n## Ожидаемый результат\nРовно один H1 на странице.\n\n## Приоритет\n2 — важно""",
                'labels': ['content']
            })
    except Exception as e:
        issues.append({
            'title': f'[BUG] Ошибка при проверке страницы {name}',
            'body': f"""## URL\n{url}\n\n## Что не так\nПри проверке страницы `{name}` произошла ошибка: {e}\n\n## Приоритет\n2 — важно""",
            'labels': ['bug']
        })

out_path = '/root/laser178-ai-framework/Logs/audit-2026-07-12.json'
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump({'url': base, 'issues_found': len(issues), 'issues': issues}, f, ensure_ascii=False, indent=2)

print('Total issues found:', len(issues))
for i in issues:
    print('-', i['title'])
