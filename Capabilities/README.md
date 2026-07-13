# Capabilities

## Назначение

Ограничивает, что Hermes может делать. Без capability — действие запрещено.

## Список

| Capability | Статус | Описание |
|------------|--------|----------|
| seo | enabled | SEO-правки title, description, H1, canonical. |
| wordpress | enabled | Read/update через WordPress Adapter. REST API запрещён. |
| content | enabled | Работа с постами и страницами. |
| security | disabled | Безопасность отключена до завершения Security Layer. |
| analytics | disabled | Аналитика отключена до предоставления доступов. |

## Использование

Authorization Engine проверяет `Capabilities/{category}.json` перед каждым действием.
