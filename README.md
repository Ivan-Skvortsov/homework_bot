<div id="top"></div>
<div align="center">
<h1>Telegram-бот</h1>
  <h3>
    Бот для отслеживания статуса домашней работы<br />
  </h3>
</div>

## О проекте
Проект представляет собой telegram-бот, который обращается к API сервиса Практикум.Домашка и узнает статус домашней работы: взята ли домашка в ревью, проверена ли она, а если проверена — то принял её ревьюер или вернул на доработку.<br />

### Основные функции бота:
 - опрос раз в 10 минут API сервиса Практикум.Домашка и проверка статуса отправленной на ревью домашней работы;
 - при обновлении статуса анализ ответа API и отправка соответствующего уведомления в Telegram;
 - логирование своей работы и отправка информации о важных проблемах сообщением в Telegram.
<p align="right">(<a href="#top">наверх</a>)</p>

## Использованные технологии и пакеты
* [Python](https://www.python.org/)
* [Python-telegram-bot](https://python-telegram-bot.org/)
<p align="right">(<a href="#top">наверх</a>)</p>

## Необходимый софт
Для запуска проекта потребутеся машина, с предустановленным интерпретатором Python</a>.

## Установка
Склонируйте проект на Ваш компьютер
   ```sh
   git clone https://github.com/Ivan-Skvortsov/homework_bot.git
   ```
Перейдите в папку с проектом
   ```sh
   cd homework_bot
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
Создайте файл с переменными окружения
   ```sh
   touch .env
   ```
Наполните файл следующими переменными
   ```sh
   PRACTICUM_TOKEN  # токен авторизации API сервиса Практикум.Домашка
   TELEGRAM_TOKEN  # токен телеграм для работы с Bot API
   TELEGRAM_CHAT_ID  # ID телеграм-чата, в который бот должен отправить сообщение
   ```
<p align="right">(<a href="#top">наверх</a>)</p>

## Использование

Запуск бота осуществляется из командной строки при помощи команды:
   ```sh
   python3 homework.py
   ```

## Об авторе
Автор проекта: Иван Скворцов<br/><br />
[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Ivan-Skvortsov/)
[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:pprofcheg@gmail.com)
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/Profcheg)
<p align="right">(<a href="#top">наверх</a>)</p>
