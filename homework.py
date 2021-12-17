import logging
import os
import sys
import time
from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv

from custom_exceptions import (ProgramVariablesNotSet, WrongResponseStatusCode,
                               WrongResponseStructure, ParseHomeworkerror)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s: [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def send_message(bot, message):
    """Sends message to telegram bot."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.info(f'Сообщение успешно отправлено в телеграм: {message}')
    except Exception as err:
        logger.error(f'Ошибка отправки сообщения в телеграм: {err}')


def get_api_answer(current_timestamp):
    """
    Request ENDPOINT API and check status of response.
    Return response content, converted to python dict.
    """
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    try:
        response = requests.get(url=ENDPOINT, headers=HEADERS, params=params)
        result = response.json()
    except Exception as err:
        logger.error(f'Ошибка обращения к основному API: {err}')
        raise
    else:
        if response.status_code != HTTPStatus.OK:
            err = (
                f'Эндпойнт {response.url} недоступен! '
                f'Код ответа: {response.status_code}'
            )
            logger.error(err)
            raise WrongResponseStatusCode(err)
        return result


def check_response(response):
    """Check structure of response. Return list of homeworks."""
    if not isinstance(response, dict):
        # Если здесь rase'ить исключение - не проходит тесты
        err = (
            'Получен неверный тип данных. Ожидаемый тип: dict.'
            f'Полученный тип: {type(response)}'
        )
        logger.error(err)
        return WrongResponseStructure(err)
    if not response:
        err = (
            'Получена неверная структура данных: словарь пуст.'
        )
        logger.error(err)
        raise WrongResponseStructure(err)
    if 'homeworks' not in response:
        err = (
            'Получена неверная структура данных: не найден ключ `homeworks`.'
        )
        logger.error(err)
        raise WrongResponseStructure(err)
    if not isinstance(response['homeworks'], list):
        hw_type = type(response['homeworks'])
        err = (
            'Получена неверная структура данных. Ожидаемый тип данных по ключу'
            f' `homeworks`: list. Полученный тип: {hw_type}'
        )
        logger.error(err)
        raise WrongResponseStructure(err)
    return response['homeworks']


def parse_status(homework):
    """Parse status of homework, returns verdict as string or None."""
    try:
        homework_name = homework['homework_name']
        homework_status = homework['status']
        verdict = VERDICTS[homework_status]
    except KeyError as err:
        logger.error(f'Ошибка обработки полученных данных: {err}')
        raise ParseHomeworkerror(err)
    except TypeError as err:
        logger.error(f'Ошибка обработки полученных данных: {err}')
        raise ParseHomeworkerror(err)
    else:
        if not homework_status:
            return None
        return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Check if enviroment variables are set."""
    return all((PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID))


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
    previous_hw_status = ''
    while True:
        try:
            response = get_api_answer(current_timestamp)
            homework_list = check_response(response)
            for homework in homework_list:
                homework_status = parse_status(homework)
                if homework_status and homework_status != previous_hw_status:
                    send_message(bot, homework_status)
                    previous_hw_status = homework_status
            current_timestamp = int(time.time())
            time.sleep(RETRY_TIME)

        except Exception as err:
            message = f'Сбой в работе программы: {err}'
            if message != previous_error_message:
                send_message(bot, message)
                previous_error_message = message
            time.sleep(RETRY_TIME)
        else:
            if not homework_list:
                logger.debug('Проверка выполнена успешно. Обновлений нет.')


if __name__ == '__main__':
    main()
