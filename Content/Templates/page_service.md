# Template: Страница услуги

## Структура

1. H1 — название услуги + регион
2. Короткое описание (2–3 предложения)
3. Для чего нужна услуга (список)
4. Как мы работаем (этапы)
5. Преимущества (3–4 пункта)
6. Часто задаваемые вопросы (FAQ)
7. CTA + контакты
8. Примечание о гарантии (если подтверждено)

## Правила

- Использовать только verified данные из `Knowledge/Company/services.yaml` и `company.yaml`.
- Не указывать цены, если `public: false` или `verified: false`.
- H1 должен содержать город для SEO (из `company.yaml.city_for_seo`).
- CTA — через фрагмент `Content/Fragments/cta.md`.
- Контакты — через фрагмент `Content/Fragments/contacts_block.md`.

## Placeholder

```markdown
# {{service.name}} в {{company.city_for_seo}}

{{service.short_description}}

## Когда нужна {{service.name}}

- ...
- ...

## Как мы работаем

1. ...
2. ...
3. ...

## Почему выбирают нас

- ...
- ...

## FAQ

**Вопрос?**
Ответ.

{{cta_fragment}}
{{contacts_fragment}}
```
