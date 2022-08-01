import logging

# Порт по умолчанию
DEFAULT_PORT = 7777

# IP-адрес по умолчанию
DEFAULT_IP_ADDRESS = '127.0.0.1'

# Максимальная очередь подключений
MAX_CONNECTIONS = 5

# Максимальная длина сообщения в байтах
MAX_PACKAGE_LENGTH = 1024

# Кодировка
ENCODING = 'utf-8'

# Основные ключи протокола JIM (JSON instant messaging):
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
SENDER = 'sender'
DESTINATION = 'to'

# Прочие ключи
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'message'
MESSAGE_TEXT = 'mess_text'
EXIT = 'exit'

# Уровень логирования
LOGGING_LEVEL = logging.DEBUG

# Словари - ответы:
# 200
RESPONSE_200 = {RESPONSE: 200}
# 400
RESPONSE_400 = {
    RESPONSE: 400,
    ERROR: None
}
