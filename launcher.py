"""Лаунчер"""

import os
import signal
import subprocess
import sys
from time import sleep


PYTHON_PATH = sys.executable
BASE_PATH = os.path.dirname(os.path.abspath(__file__))


def get_subprocess(file_with_args):
    sleep(0.2)
    file_full_path = f"{PYTHON_PATH} {BASE_PATH}/{file_with_args}"
    args = ["gnome-terminal", "--disable-factory", "--", "bash", "-c", file_full_path]
    return subprocess.Popen(args, preexec_fn=os.setpgrp)


process = []
while True:
    TEXT_FOR_INPUT = "Выберите действие: q - выход, s - запустить сервер и клиенты, x - закрыть все окна: "
    action = input(TEXT_FOR_INPUT)

    if action == "q":
        break
    elif action == "s":
        process.append(get_subprocess("server.py"))

        for i in range(2):
            process.append(get_subprocess(f"client.py -n test{i+1}"))

    elif action == "x":
        while process:
            victim = process.pop()
            os.killpg(victim.pid, signal.SIGINT)


# для windows
#
# import subprocess
#
# PROCESS = []
#
# while True:
#     ACTION = input('Выберите действие: q - выход, '
#                    's - запустить сервер и клиенты, x - закрыть все окна: ')
#
#     if ACTION == 'q':
#         break
#     elif ACTION == 's':
#         PROCESS.append(subprocess.Popen('python server.py',
#                                         creationflags=subprocess.CREATE_NEW_CONSOLE))
#         for i in range(2):
#             PROCESS.append(subprocess.Popen('python client.py -m send',
#                                             creationflags=subprocess.CREATE_NEW_CONSOLE))
#         for i in range(5):
#             PROCESS.append(subprocess.Popen('python client.py -m listen',
#                                             creationflags=subprocess.CREATE_NEW_CONSOLE))
#     elif ACTION == 'x':
#         while PROCESS:
#             VICTIM = PROCESS.pop()
#             VICTIM.kill()
