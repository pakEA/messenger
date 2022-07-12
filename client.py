"""Программа-клиент"""

import sys
import json
import time
import logging

from socket import socket, AF_INET, SOCK_STREAM
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, DEFAULT_IP_ADDRESS
from common.utils import get_message, send_message
from project_logs.config import client_log_config
from decors import log

# Инициализируем логгер
LOGGER = logging.getLogger('messenger.client')


@log
def create_presence(account_name='Guest'):
    """
    Функция генерирует запрос о присутствии клиента.
    :param account_name:
    :return:
    """
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    LOGGER.debug(f'Сформировано "{PRESENCE}" сообщение для'
                        f'пользователя: {account_name}')
    return out


@log
def process_ans(message):
    """
    Функция разбирает ответ сервера.
    :param message:
    :return:
    """
    LOGGER.debug(f'Получено сообщение от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200: OK'
        return f'400: {message[ERROR]}'
    raise ValueError


def main():
    """
    Функция загружает параметры командной строки.
    :return:
    """
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if 1024 > server_port > 65535:
            LOGGER.critical(f'Порт "{server_port}" находится вне '
                                   f'диапазона от 1024 до 65535')
            raise ValueError
    except IndexError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        LOGGER.warning('В качестве порта может быть указано только '
                              'число в диапазоне от 1024 до 65535!')
        sys.exit(1)

    # Инициализация сокета и обмен
    transport = socket(AF_INET, SOCK_STREAM)
    transport.connect((server_address, server_port))
    message_to_server = create_presence()
    send_message(transport, message_to_server)
    try:
        answer = process_ans(get_message(transport))
        LOGGER.debug(f'Получен ответ от сервера "{answer}"')
    except(ValueError, json.JSONDecodeError):
        LOGGER.error('Не удалось расшифровать сообщение сервера.')


if __name__ == '__main__':
    main()
