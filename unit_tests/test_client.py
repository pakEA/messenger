"""Unit-тесты клиента"""

import sys
import os
import unittest

from common.variables import RESPONSE, ERROR, USER, ACCOUNT_NAME, \
    TIME, ACTION, PRESENCE
from client import create_presence, process_ans

sys.path.append(os.path.join(os.getcwd(), '..'))


class TestClient(unittest.TestCase):
    """Класс с тестами для клиента"""

    def test_create_presence(self):
        """Тест корректного запроса"""
        test = create_presence()
        test[TIME] = '13.56'    # время необходимо захардкодить,
                                # иначе тест не пройдет
        self.assertEqual(test, {ACTION: PRESENCE, TIME: '13.56',
                                USER: {ACCOUNT_NAME: 'Guest'}})

    def test_200_ans(self):
        """Тест корректного разбора ответа 200"""
        self.assertEqual(process_ans({RESPONSE: 200}), '200: OK')

    def test_400_ans(self):
        """Тест корректного разбора ответа 400"""
        self.assertEqual(process_ans(
            {RESPONSE: 400, ERROR: 'Bad Request'}),
            '400: Bad Request')

    def test_no_response(self):
        """Тест поимки исключения без поля RESPONSE"""
        self.assertRaises(ValueError, process_ans, {ERROR: 'Bad Request'})


if __name__ == '__main__':
    unittest.main()
