<div id="top"></div>
<div align="center">
<h1>Telegram-бот</h1>
  <h3>
    Бот для отслеживания статуса домашней работы<br />
  </h3>
</div>

## О проекте
Проект представляет собой парсер веб-сайта peps.python.org на базе фреймворка Scrapy. В рамках проекта реализован парсер, собирающий сводные данные по PEP. Данные сохраняются в два csv-файла: в первом файле сохраняется список всех PEP (номер, название и статус), во втором - сводные данные по статусам РЕР (сколько найдено документов в каждом статусе).
<p align="right">(<a href="#top">наверх</a>)</p>

## Использованные технологии и пакеты
* [Python](https://www.python.org/)
* [Scrapy](https://scrapy.org/)
<p align="right">(<a href="#top">наверх</a>)</p>

## Необходимый софт
Для запуска проекта потребутеся машина, с предустановленным интерпретатором Python</a>.

## Установка
Склонируйте проект на Ваш компьютер
   ```sh
   git clone https://github.com/Ivan-Skvortsov/scrapy_parser_pep.git
   ```
Перейдите в папку с проектом
   ```sh
   cd scrapy_parser_pep
   ```
Активируйте виртуальное окружение
   ```sh
   python3 -m venv venv
   ```
   ```sh
   source venv/bin/activate
   ```
Обновите менеджер пакетов (pip)
   ```sh
   pip3 install --upgrade pip
   ```
Установите необходимые зависимости
   ```sh
   pip3 install -r requirements.txt
   ```
<p align="right">(<a href="#top">наверх</a>)</p>

## Использование

Запуск парсера осуществляется из командной строки при помощи команды::
   ```sh
   scrapy crawl pep
   ```
Результаты работы парсера будут сохранены в csv-файлах в папке results

## Об авторе
Автор проекта: Иван Скворцов<br/><br />
[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Ivan-Skvortsov/)
[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:pprofcheg@gmail.com)
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/Profcheg)
<p align="right">(<a href="#top">наверх</a>)</p>
