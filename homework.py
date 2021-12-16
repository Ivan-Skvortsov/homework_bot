import os
import sys
import time
import logging
import requests
import telegram
from custom_exceptions import (
    ProgramVariablesNotSet,
    SendMessageError,
    WrongResponseStatusCode,
    WrongResponseStructure
)

from http import HTTPStatus
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s: [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


RETRY_TIME = 10  # 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def send_message(bot, message):
    """Sends message to telegram bot."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
    except Exception as err:
        raise SendMessageError(err)


def get_api_answer(current_timestamp):
    """
    Request ENDPOINT API and check status of response.
    Return response content, converted to python dict.
    """
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    response = requests.get(url=ENDPOINT, headers=HEADERS, params=params)
    if response.status_code != HTTPStatus.OK:
        raise WrongResponseStatusCode(
            f'Эндпойнт {response.url} недоступен! '
            f'Код ответа: {response.status_code}'
        )
    return response.json()


def check_response(response):
    """Check structure of response. Return list of homeworks."""
    if not isinstance(response, dict):
        # Если здесь rase'ить исключение - не проходит тесты
        return WrongResponseStructure(
            'Получен неверный тип данных. Ожидаемый тип: dict.'
            f'Полученный тип: {type(response)}'
        )
    if not response:
        raise WrongResponseStructure(
            'Получена неверная структура данных: словарь пуст.'
        )
    if 'homeworks' not in response:
        raise WrongResponseStructure(
            'Получена неверная структура данных: не найден ключ `homeworks`.'
        )
    if not isinstance(response['homeworks'], list):
        hw_type = type(response['homeworks'])
        raise WrongResponseStructure(
            'Получена неверная структура данных. Ожидаемый тип данных по ключу'
            f' `homeworks`: list. Полученный тип: {hw_type}'
        )
    return response['homeworks']


def parse_status(homework):
    """Parse status of homework, returns verdict as string or None."""
    homework_name = homework['homework_name']
    homework_status = homework['status']
    verdict = HOMEWORK_STATUSES[homework_status]
    if not homework_status:
        return None
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Check if enviroment variables are set."""
    return None not in (PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)


def main():
    """Main logic of program."""
    logger.info('Программа запущена.')

    if not check_tokens():
        msg = 'Ошибка! Отсутствуют необходимые переменные окружения!'
        logger.critical(msg)
        raise ProgramVariablesNotSet(msg)

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    previous_error_message = ''
    while True:
        try:
            response = get_api_answer(current_timestamp)
            homework_list = check_response(response)
            for homework in homework_list:
                homework_status = parse_status(homework)
                if homework_status:
                    send_message(bot, homework_status)
                    logger.info(
                        f'Сообщение успешно отправлено в телеграм:'
                        f' {homework_status}'
                    )
            current_timestamp = int(time.time())
            time.sleep(RETRY_TIME)

        except SendMessageError as err:
            logger.error(f'Ошибка отправки сообщения в телеграм: {err}')
            time.sleep(RETRY_TIME)

        except Exception as err:
            message = f'Сбой в работе программы: {err}'
            if message != previous_error_message:
                send_message(bot, message)
                previous_error_message = message
            logger.error(message)
            time.sleep(RETRY_TIME)
        else:
            if not homework_list:
                logger.debug('Проверка выполнена успешно. Обновлений нет.')


if __name__ == '__main__':
    main()
