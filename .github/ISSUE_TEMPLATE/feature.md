name: Новая функция / блок / интеграция
description: Добавить новый блок, калькулятор, виджет, интеграцию
title: '[FEATURE] '
labels: ['feature']
body:
  - type: input
    id: url
    attributes:
      label: URL страницы (если применимо)
      placeholder: 'https://laser178.ru/'
  - type: textarea
    id: description
    attributes:
      label: Что нужно сделать
      placeholder: 'Добавить квиз подбора защиты на главную'
    validations:
      required: true
  - type: textarea
    id: reason
    attributes:
      label: Зачем / какая цель
      placeholder: 'Увеличить заявки, упростить выбор услуги'
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
  - type: textarea
    id: references
    attributes:
      label: Референсы / примеры
      placeholder: 'Ссылки на похожие решения'
