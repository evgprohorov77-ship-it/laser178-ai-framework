name: Контент / SEO / текст
description: Правки title, description, текста страницы, статьи блога
title: '[CONTENT] '
labels: ['content']
body:
  - type: input
    id: url
    attributes:
      label: URL страницы
      placeholder: 'https://laser178.ru/services/'
    validations:
      required: true
  - type: dropdown
    id: type
    attributes:
      label: Тип правки
      options:
        - Title
        - Meta description
        - H1/H2
        - Основной текст
        - FAQ
        - Теги
        - Статья блога
    validations:
      required: true
  - type: textarea
    id: task
    attributes:
      label: Что сделать
      placeholder: 'Изменить title на ...'
    validations:
      required: true
  - type: textarea
    id: draft
    attributes:
      label: Черновик / идеи
      placeholder: 'Вставь предлагаемый текст или ключевые слова'
  - type: dropdown
    id: priority
    attributes:
      label: Приоритет
      options:
        - '1 — критично'
        - '2 — важно'
        - '3 — можно подождать'
    validations:
      required: true
