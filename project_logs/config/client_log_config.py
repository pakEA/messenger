"""Конфиг для логгера клиента"""

import logging
import os
import sys
import pathlib

from common.variables import LOGGING_LEVEL

sys.path.append('../')

# path = os.path.dirname(os.path.abspath(__file__))
path = pathlib.Path.cwd() / 'project_logs' / 'logs'
print(path)
path = os.path.join(path, 'client.log')
# print(path)

# создаем именованный логгер
logger = logging.getLogger('messenger.client')

# задаем формат
client_formatter = logging.Formatter(
    '%(asctime)-30s %(levelname)-10s %(module)-20s %(message)s')

# создаем обработчик
file_handler = logging.FileHandler(path, encoding='utf-8')
file_handler.setLevel(LOGGING_LEVEL)

# подключаем формат к обработчику
file_handler.setFormatter(client_formatter)

# добавляем обработчик к логгеру
logger.addHandler(file_handler)
logger.setLevel(LOGGING_LEVEL)

# отладка
if __name__ == '__main__':
    logger.info('Инфо')
    logger.debug('Отладка')
    logger.error('Ошибка')
    logger.critical('Критично')
