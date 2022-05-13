"""Программа-сервер"""

import sys
import json
from socket import socket, AF_INET, SOCK_STREAM
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, \
    MAX_CONNECTIONS, PRESENCE, TIME, USER, ERROR, DEFAULT_PORT
from common.utils import get_message, send_message


def proccess_client_message(message):
    """
    Функция принимает словарь (сообщение от клиента), проверяет корректность,
    возвращает словарь для ответа клинету
    :param message:
    :return:
    """
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
            raise ValueError
    except IndexError:
        print('После параметра "-p" необходимо указать номер порта')
        sys.exit(1)
    except ValueError:
        print('В качестве порта может быть указано только число в '
              'диапазоне от 1024 до 65535!')
        sys.exit(1)

    # Загружаем какой адрес слушать
    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''
    except IndexError:
        print('После параметра "-a" необходимо указать адрес, '
              'который будет слушать сервер')
        sys.exit(1)

    # Готовим сокет
    transport = socket(AF_INET, SOCK_STREAM)
    transport.bind((listen_address, listen_port))

    # Слушаем порт
    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        try:
            message_from_client = get_message(client)
            print(message_from_client)
            response = proccess_client_message(message_from_client)
            send_message(client, response)
            client.close()
        except(ValueError, json.JSONDecodeError):
            print('Принято некорректное сообщение от клиента.')
            client.close()


if __name__ == '__main__':
    main()
