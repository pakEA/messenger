"""Unit-тесты сервера"""

import sys
import os
import unittest

from common.variables import RESPONSE, ERROR, USER, ACCOUNT_NAME, \
    TIME, ACTION, PRESENCE
from server import proccess_client_message

sys.path.append(os.path.join(os.getcwd(), '..'))


class TestServer(unittest.TestCase):
    """Класс с тестами для сервера"""

    err_dict = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

    ok_dict = {
        RESPONSE: 200
    }

    def test_no_action(self):
        """Ошибка если нет действия"""
        self.assertEqual(proccess_client_message(
            {TIME: '12.24', USER: {ACCOUNT_NAME: 'Guest'}}),
            self.err_dict)

    def test_wrong_action(self):
        """Ошибка при неизвестном действии"""
        self.assertEqual(proccess_client_message(
            {ACTION: 'Wrong', TIME: '12.24', USER: {ACCOUNT_NAME: 'Guest'}}),
            self.err_dict)

    def test_no_time(self):
        """Ошибка если нет времени"""
        self.assertEqual(proccess_client_message(
            {ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Guest'}}),
            self.err_dict)

    def test_no_user(self):
        """Ошибка если нет юзера"""
        self.assertEqual(proccess_client_message(
            {ACTION: PRESENCE, TIME: '12.24'}),
            self.err_dict)

    def test_unknown_user(self):
        """Ошибка если юзер не 'Guest'"""
        self.assertEqual(proccess_client_message(
            {ACTION: PRESENCE, TIME: '12.24', USER: {ACCOUNT_NAME: 'Guest_1'}}),
            self.err_dict)

    def test_ok_check(self):
        """Корректный запрос"""
        self.assertEqual(proccess_client_message(
            {ACTION: PRESENCE, TIME: '12.24', USER: {ACCOUNT_NAME: 'Guest'}}),
            self.ok_dict)


if __name__ == '__main__':
    unittest.main()
