import json
from common.variables import MAX_PACKAGE_LENGTH, ENCODING
from decors import log


@log
def get_message(client):
    """
    Функция принимает байты и выдает словарь, если принято что-то другое
    выдает ошибку значения.
    :param client:
    :return:
    """
    encoded_response = client.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


@log
def send_message(sock, message):
    """
    Функция принимает словарь и отправляет его
    :param sock:
    :param message:
    :return:
    """
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)
