# План публикации контента

## Сгенерированные черновики

### Страницы (Pages)
| Файл | Статус |
|------|--------|
| `service_disassembly.md` | draft ✅ verified |
| `service_laser_cleaning.md` | draft ✅ verified |
| `service_anticor_complex.md` | draft ✅ verified |
| `service_cavity_conservation.md` | draft ✅ verified |
| `page_guarantee.md` | draft ✅ verified |
| `page_contact.md` | draft ✅ verified |
| `page_price.md` | draft ⚠️ цены не public |

### Статьи (Articles)
| Файл | Категория | Статус |
|------|-----------|--------|
| `article_toyota_camry.md` | База по моделям | draft ✅ verified |
| `article_bmw_x5.md` | База по моделям | draft ✅ verified |
| `article_lada_vesta.md` | База по моделям | draft ✅ verified |
| `article_kia_rio.md` | База по моделям | draft ✅ verified |
| `article_skoda_octavia.md` | База по моделям | draft ✅ verified |
| `article_hyundai_creta.md` | База по моделям | draft ✅ verified |
| `article_likbez_laser_cleaning.md` | Ликбез | draft ✅ verified |
| `article_faq_common.md` | FAQ | draft ✅ verified |

## Проверка

```bash
find Content/Drafts -name '*.md' -print0 | xargs -0 -I {} python3 Scripts/check_content.py {}
```

Результат: ✅ 15 из 15 черновиков прошли проверку.

## Рекомендации по публикации

1. **page_price.md** — цены отмечены как «от ... ₽», потому что в `Owner/pricing.yaml` все цены `public: false`.  
   Для публикации точного прайса установи `public: true` на нужные позиции в Owner Portal и синхронизируй.

2. **page_guarantee.md** — гарантийные условия общие. Для точных формулировок заполни `Owner/guarantees.yaml`.

3. **Статьи по моделям** — готовы к публикации, но не содержат конкретных цен. Можно добавить цены после верификации pricing.

4. **Перед публикацией** каждый черновик требует owner approval.

## Следующие шаги

- Owner review и approval.
- Вручную добавить статьи в WordPress / Elementor или через WordPress Adapter после Security Layer.
- После публикации перенести файлы в `Content/Published/` и зафиксировать в Changelog.
