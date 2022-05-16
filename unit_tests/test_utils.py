""""""

import sys
import os
import unittest
import json

from common.variables import RESPONSE, ERROR, USER, ACCOUNT_NAME, \
    TIME, ACTION, PRESENCE, ENCODING
from common.utils import get_message, send_message

sys.path.append(os.path.join(os.getcwd(), '..'))


class TestSocket:
    """
    Тестовый класс для тестирования отправки и получения сообщений,
    при создании требует словарь, который пойдет в тестовую функцию
    """
    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.receved_message = None

    def send(self, message_to_send):
        """
        Функция отправки, кодирует сообщение, а также сохраняет что
        должно было отправленрв сокет
        :param message_to_send: - то, что отправляем в сокет
        :return:
        """
        json_test_massage = json.dumps(self.test_dict)

        # кодируем сообщение
        self.encoded_message = json_test_massage.encode(ENCODING)

        # сохраняем то, что должно было отправлено в сокет
        self.receved_message = message_to_send

    def recv(self, max_len):
        """
        Получаем данные из сокета
        :param max_len:
        :return:
        """
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode(ENCODING)


class TestUtils(unittest.TestCase):
    """Тестовый класс, выполняющий тестирование"""
    test_dict_send = {
        ACTION: PRESENCE,
        TIME: '10.45',
        USER: {ACCOUNT_NAME: 'Guest'}
     }

    test_dict_recv_ok = {RESPONSE: 200}
    test_dict_recv_err = {RESPONSE: 400, ERROR: 'Bad Request'}

    def test_send_massage(self):
        """
        Тестируем корректность работы функции отправки.
        Создадим тестовый сокет и проверим корректность отправки словаря
        :return:
        """
        test_socket = TestSocket(self.test_dict_send)  # экземпляр тестового словаря
        send_message(test_socket, self.test_dict_send)  # вызов тестируемой функции

        # сравниваем результат доверенного кодирования и результат от тестируемой функции
        self.assertEqual(test_socket.encoded_message, test_socket.receved_message)

        # проверяем генерацию исключения, если на входе пришел не словарь
        with self.assertRaises(Exception):
            send_message(test_socket, test_socket)

    def test_get_massage(self):
        """
        Тест функции приема сообщения
        :return:
        """
        test_sock_ok = TestSocket(self.test_dict_recv_ok)
        test_sock_err = TestSocket(self.test_dict_recv_err)

        # тест корректной расшифровки корректного словаря
        self.assertEqual(get_message(test_sock_ok), self.test_dict_recv_ok)

        # тест корректной расшифровки некорректного словаря
        self.assertEqual(get_message(test_sock_err), self.test_dict_recv_err)


if __name__ == '__main__':
    unittest.main()
