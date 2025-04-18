# 🤖 CV-Analyzer: Анализ компетенций по матрице Альянса ИИ
---
- Проект по хакатону от Газпром Нефти и СПбГЭУ
- Интерактивное веб-приложение на базе Streamlit для автоматизированного анализа резюме и определения уровня владения ИИ-компетенциями. Основано на модели, обученной по матрице компетенций Альянса ИИ, с возможностью персонализированных рекомендаций, визуализации соответствия профессиям и интеграцией GitHub-профиля пользователя.
---
## 🔗 Ссылки

[Веб‑приложение](https://cv-analyzer-gazprom-neft.streamlit.app/)  [![🌙 Dark Mode Recommended](https://img.shields.io/badge/theme-dark-blue?style=flat&logo=github)](https://cv-analyzer-gazprom-neft.streamlit.app/) [![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat)](https://cv-analyzer-gazprom-neft.streamlit.app/)

> **Рекомендуем** использовать **тёмную тему** для наилучшего восприятия контента.

[Документация в Google Docs](https://docs.google.com/document/d/1lgbiqXAzj9J_sWFw-ep4w4qTQOpA2A_-5ieAzwoP62M/edit?tab=t.0)
[![Google Docs](https://img.shields.io/badge/Google%20Docs-blue?style=flat)](https://docs.google.com/document/d/1lgbiqXAzj9J_sWFw-ep4w4qTQOpA2A_-5ieAzwoP62M/edit?tab=t.0)

[Презентация по хакатону]()
[![PowerPoint](https://img.shields.io/badge/PowerPoint-darkorange?style=flat&logo=microsoft-powerpoint)](https://www.office.com/launch/powerpoint?auth=2&appid=ВАШ_ИД_ПРЕЗЕНТАЦИИ)

---

## Возможности

- Загрузка и анализ резюме (PDF, DOCX, TXT)
- Определение ИИ-компетенций на основе обученной модели
- Самостоятельная корректировка грейдов (0–3)
- Интеграция с GitHub: автоматический анализ `README.md` из репозиториев
- Визуализация соответствия профессиям по матрице
- Рекомендации по развитию слабых компетенций
- Возможность расширения с помощью интерпретируемости (LIME, Attention) — сейчас в веб-приложении отсутствует, ибо streamlit не выдерживает и падает

## Проблематика и целевая аудиторий

| **Проблематика**                                                                              | **Целевая аудитория**                                           |
|-----------------------------------------------------------------------------------------------|-----------------------------------------------------------------|
| **Сложности с подбором IT‑специалистов**<br>Компании не успевают находить кандидатов с актуальными навыками.     | • Руководители отделов<br>• Технические интервьюеры             |
| **Разрыв образования и рынка**<br>Учебные программы вузов и онлайн‑курсов отстают от трендов Big Data, ИИ, DevOps. | • HR‑специалисты и рекрутеры<br>• Аналитики по подбору персонала |
| **Необходимость автоматизации**<br>При большом потоке резюме сложно оперативно отобрать лучших кандидатов.      |                                                                 |


## Функции и преимущества

| **Функции**                                                                                                | **Преимущества**                                                   |
|------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------|
| • Сопоставление компетенций кандидатов с требованиями вакансий                                             | • Снижение времени на отбор кандидатов                             |
| • Генерация персональных карьерных рекомендаций                                                            | • Повышение точности и релевантности подбора                       |
| • Автоматизация обратной связи кандидатам и сотрудникам                                                    | • Сокращение затрат на внешних рекрутеров                          |
| • Анализ и прогнозирование карьерных траекторий сотрудников                                                 | • Оптимизация обучения и повышения квалификации                    |
| • Предложение курсов и сертификаций для устранения «skill‑gap»                                              | • Повышение качества обратной связи                                |
|                                                                                                            | • Улучшение долгосрочной карьерной стратегии сотрудников           |

## Структура проекта

```plaintext
CV-ANALYZER-GAZPROM-NEFT/
├── .streamlit/                # Конфигурации Streamlit с доп. настройками
│   └── config.toml
├── others/                    # Прочие ресурсы проекта
├── utils/                     # Вспомогательные модули и логика
│   ├── __init__.py            # Инициализация пакета
│   ├── constants.py           # Список компетенций, матрица профессий и рекомендации
│   ├── cv_reader.py           # Извлечение и очистка текста из резюме
│   ├── github_reader.py       # Поиск и парсинг GitHub-профиля пользователя
│   ├── explanation.py         # Интерпретируемость модели (LIME, Attention)
│   ├── model_service.py       # Загрузка модели, предсказания с учётом threshold
│   └── resume_processor.py    # Объединение резюме + GitHub текстов
├── app.py                     # Основной Streamlit-приложение
├── requirements.txt           # Список зависимостей Python
└── README.md                  # Документация проекта
```

## Requirements

```bash
streamlit
transformers
huggingface-hub
torch
matplotlib
seaborn
scikit-learn
pdfminer.six
python-docx
requests
numpy
mplcyberpunk
lime
```
---

## Наша команда

<table>
  <tr>
    <td align="center">
      <img src="https://github.com/KsyLight.png?size=100" width="100" alt="Егор"/>
      <p><strong>Егор</strong><br/><a href="https://github.com/KsyLight">KsyLight</a></p>
    </td>
    <td align="center">
      <img src="https://github.com/Akim-norfeg.png?size=100" width="100" alt="Аким"/>
      <p><strong>Аким</strong><br/><a href="https://github.com/Akim-norfeg">Akim-norfeg</a></p>
    </td>
    <td align="center">
      <img src="https://github.com/Swagozavr.png?size=100" width="100" alt="Максим"/>
      <p><strong>Максим</strong><br/><a href="https://github.com/Swagozavr">Swagozavr</a></p>
    </td>
    <td align="center">
      <img src="https://github.com/klevkina.png?size=100" width="100" alt="Катя"/>
      <p><strong>Катя</strong><br/><a href="https://github.com/klevkina">klevkina</a></p>
    </td>
    <td align="center">
      <img src="https://github.com/kwarkw.png?size=100" width="100" alt="Аня"/>
      <p><strong>Аня</strong><br/><a href="https://github.com/kwarkw">kwarkw</a></p>
    </td>
  </tr>
</table>

<p align="center">
  <img src="others/cat.jpg" alt="Котик AI" width="200" />
</p>
