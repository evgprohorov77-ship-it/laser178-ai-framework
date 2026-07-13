# Content Layer

## Версия

1.0.0

## Назначение

Content Layer — это слой черновиков, шаблонов и готового к публикации контента.  
Он строится на основе **verified** Knowledge и не требует новых Engines или Adapters.

## Структура

```
Content/
├── README.md
├── Templates/              # Повторно используемые шаблоны
│   ├── page_service.md
│   ├── page_price.md
│   ├── page_guarantee.md
│   ├── page_contact.md
│   ├── article_model.md
│   ├── article_lab.md
│   ├── article_likbez.md
│   ├── article_case.md
│   └── article_faq.md
├── Drafts/                 # Черновики, сгенерированные Hermes
│   ├── Pages/
│   └── Articles/
├── Published/              # Утверждённые и опубликованные материалы (только owner)
│   └── index.md
└── Fragments/              # Маленькие блоки: CTA, контакты, отзыв, вставка
    ├── cta.md
    ├── contacts_block.md
    └── guarantee_notice.md
```

## Принципы

1. **Все материалы — производные от Knowledge.**
2. **Перед публикацией — owner approval.**
3. **Hermes не публикует автоматически.**
4. **Каждый черновик проверяется через `check_content.py`.**
5. **Шаблоны определяют структуру, не фабрикуют факты.**

## Процесс

```
Knowledge (verified)
       ↓
Content Template
       ↓
Hermes generates draft
       ↓
check_content.py
       ↓
Owner review
       ↓
Owner approval
       ↓
Operator publishes (manual or post-Security Layer)
       ↓
Published/ + Changelog
```

## Категории блога «Бортовой журнал»

| Категория | Шаблон | Описание |
|-----------|--------|----------|
| База по моделям | `article_model.md` | Про конкретную марку/модель (Camry, X5, Vesta и т.д.) |
| Лаборатория | `article_lab.md` | Тесты, сравнения материалов, эксперименты |
| Ликбез | `article_likbez.md` | Объяснения технологий и терминов |
| Кейс | `article_case.md` | Before/After, история конкретного автомобиля |
| FAQ | `article_faq.md` | Ответы на частые вопросы |

## Статусы черновиков

| Статус | Описание |
|--------|----------|
| `draft` | Сгенерирован, не проверен |
| `review` | Проверен через check_content.py, ожидает owner review |
| `approved` | Owner approved, готов к публикации |
| `published` | Опубликован на сайте |
| `archived` | Устарел, не используется |

## Пример использования

```bash
# Сгенерировать черновик страницы услуги
python3 Scripts/generate_content.py --template page_service --service laser_cleaning

# Проверить черновик
python3 Scripts/check_content.py Content/Drafts/Pages/service_laser_cleaning.md
```

## Примечание

Content Layer не подключается к WordPress напрямую.  
Публикация выполняется вручную Operator или через WordPress Adapter после Security Layer.
