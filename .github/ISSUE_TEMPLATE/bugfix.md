name: Визуальный/технический баг
description: Ошибка вёрстки, битая ссылка, JS, CSS, мобильная версия
title: '[BUG] '
labels: ['bug']
body:
  - type: input
    id: url
    attributes:
      label: URL страницы
      placeholder: 'https://laser178.ru/'
    validations:
      required: true
  - type: input
    id: selector
    attributes:
      label: CSS-селектор элемента (если есть)
      placeholder: 'img#laserLightboxImg'
  - type: textarea
    id: problem
    attributes:
      label: Что не так
      placeholder: 'На мобильном тап по фото блокирует скролл'
    validations:
      required: true
  - type: textarea
    id: expected
    attributes:
      label: Ожидаемый результат
      placeholder: 'Скролл должен работать; лайтбокс открываться только по тапу'
    validations:
      required: true
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
    id: screenshot
    attributes:
      label: Скриншот/пометка
      placeholder: 'Вставь ссылку на изображение или текст пометки'
