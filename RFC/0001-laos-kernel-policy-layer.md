# RFC-0001: LAOS Kernel — Policy Layer, Authorization, Dry Run, Backup, Approval

## Статус

Approved

## Автор

Hermes LAOS

## Дата

2026-07-13

## Краткое описание

Создать LAOS Kernel: Policy Layer, Authorization Engine, Dry Run Engine, Backup Engine, Approval System, Production Lock, Environment, Capability System и разбить Knowledge на базу данных.

## Мотивация

Система безопасности ещё не завершена. Нельзя подключать WordPress REST API и выполнять реальные изменения на сайте до завершения Policy Layer.

## Предлагаемое решение

1. Создать `Policies/` с 8 документами.
2. Создать `AI/Authorization/`, `AI/DryRun/`, `AI/Backup/`, `AI/Approval/`.
3. Создать `Environment/` и `Capabilities/`.
4. Создать `RFC/` и процесс.
5. Разбить `Knowledge/company.md` на `Knowledge/Company/`.

## Риски

- Увеличение сложности фреймворка.
- Задержка реальных изменений на сайте.

## Митигация

- Все Engine в MVP симулируют действия, не трогают сайт.
- Production Lock активен по умолчанию.
- Capability security отключена до завершения Security Layer.

## Статус реализации

Implemented.
