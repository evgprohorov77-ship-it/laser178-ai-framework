# Owner Template

## Как использовать

1. Скопируй этот файл в `Owner/<name>.yaml`.
2. Заполни блоки, которые относятся к твоей сущности.
3. Не удаляй обязательные поля: id, version, source, owner_portal.
4. Оставь null или закомментируй поля, которые пока не заполняешь.

## Пример YAML

См. Owner/company_profile.yaml или любой другой заполненный файл.

## Правила заполнения

- value — значение поля.
- public: true/false — публиковать ли на сайте.
- note — примечание для Hermes.
- Не используй verified / source — они проставляются Hermes при синхронизации.

## После редактирования

Запусти или попроси Hermes запустить:

    python3 Scripts/sync_owner_to_knowledge.py

Или просто скажи в Telegram: синхронизируй Owner Portal.
