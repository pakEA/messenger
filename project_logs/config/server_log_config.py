"""Конфиг для логгера сервера"""

import logging
import logging.handlers
import os
import sys
import pathlib

from common.variables import LOGGING_LEVEL

sys.path.append('../')

path = pathlib.Path.cwd() / 'project_logs' / 'logs'
# path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, 'server.log')

# создаем именованный логгер
logger = logging.getLogger('messenger.server')

# задаем формат сообщений лога
server_formatter = logging.Formatter(
    '%(asctime)-30s %(levelname)-10s %(module)-20s %(message)s')

# создаем обработчик
file_handler = logging.handlers.TimedRotatingFileHandler(
    path, encoding='utf-8', interval=1, when='midnight')
file_handler.setLevel(LOGGING_LEVEL)

# подключаем формат к обработчику
file_handler.setFormatter(server_formatter)

# добавляем обработчик к логгеру
logger.addHandler(file_handler)
logger.setLevel(LOGGING_LEVEL)

# отладка
if __name__ == '__main__':
    logger.info('Инфо')
    logger.debug('Отладка')
    logger.error('Ошибка')
    logger.critical('Критично')
