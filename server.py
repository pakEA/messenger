"""Программа-сервер"""

import sys
import json
import logging

from socket import socket, AF_INET, SOCK_STREAM
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, \
    MAX_CONNECTIONS, PRESENCE, TIME, USER, ERROR, DEFAULT_PORT
from common.utils import get_message, send_message
from project_logs.config import server_log_config
from decors import log


# Инициализируем логгер
LOGGER = logging.getLogger('messenger.server')


@log
def proccess_client_message(message):
    """
    Функция принимает словарь (сообщение от клиента), проверяет корректность,
    возвращает словарь для ответа клинету
    :param message:
    :return:
    """
    LOGGER.debug(f'Проверка сообщения от клиента: {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def main():
    """
    Функция загружает параметры командной строки, если нет параметров -
    задаем значения по умолчанию.
    :return:
    """
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if 1024 > listen_port > 65535:
            LOGGER.critical(f'Порт "{listen_port}" находится вне '
                                   f'диапазона от 1024 до 65535')
            raise ValueError
    except IndexError:
        LOGGER.info('После параметра "-p" необходимо указать номер порта')
        sys.exit(1)
    except ValueError:
        LOGGER.warning('В качестве порта может быть указано только число в '
                              'диапазоне от 1024 до 65535!')
        sys.exit(1)

    # Загружаем какой адрес слушать
    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''
    except IndexError:
        LOGGER.info('После параметра "-a" необходимо указать адрес, '
                           'который будет слушать сервер')
        sys.exit(1)

    # Готовим сокет
    transport = socket(AF_INET, SOCK_STREAM)
    transport.bind((listen_address, listen_port))

    # Слушаем порт
    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        LOGGER.info(f'Установлено соединение с: {client_address}')
        try:
            message_from_client = get_message(client)
            LOGGER.debug(f'Получено сообщение от клиента: '
                                f'{message_from_client}')
            response = proccess_client_message(message_from_client)
            LOGGER.info(f'Сформирован ответ клиенту: {response}')
            send_message(client, response)
            client.close()
        except(ValueError, json.JSONDecodeError):
            LOGGER.error('Принято некорректное сообщение от клиента.')
            client.close()


if __name__ == '__main__':
    main()
