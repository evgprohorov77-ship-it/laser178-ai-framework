# Auditors

Каждый аудитор — отдельная зона ответственности.
Все аудиторы наследуют `BaseAuditor` и возвращают `List[Finding]`.

## Список аудиторов

| Модуль | Назначение |
|--------|------------|
| `seo_auditor.py` | Title, description, H1, canonical, OG |
| `structure_auditor.py` | Битые ссылки, редиректы, дубли |
| `images_auditor.py` | ALT, SRC, размеры |
| `performance_auditor.py` | robots.txt, sitemap.xml, время ответа |
| `security_auditor.py` | generator, xmlrpc, утечки версий |
| `wordpress_auditor.py` | Доступность wp-admin, плагины, тема |

## Запуск

```python
from Auditors.runner import AuditRunner
runner = AuditRunner()
findings = runner.run_page("https://laser178.ru/")
```

## Требования

- Произвольные словари запрещены.
- Каждый Finding должен содержать `framework_reference`.
- Severity только P0–P3.
- Confidence в диапазоне [0.0, 1.0].
