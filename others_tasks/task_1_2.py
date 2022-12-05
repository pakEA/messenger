"""
Написать функцию host_range_ping() для перебора ip-адресов из заданного
диапазона. Меняться должен только последний октет каждого адреса. По
результатам проверки должно выводиться соответствующее сообщение.
"""

from ipaddress import ip_address
from task_1_1 import host_ping


def host_range_ping():
    host_list = []
    begin_ip = input('Введите начальный адрес: ')
    while True:
        try:
            last_octet = int(begin_ip.split('.')[3])
            break
        except Exception as exp:
            print(exp)

    while True:
        finish_ip = int(input('Сколько адресов проверить? Введите число: '))

        if (last_octet + finish_ip) > 254:
            print('Можно менять только последний октет! '
                  f'Максимальное число адресов для проверки - {254-last_octet}')
        else:
            break

    for i in range(finish_ip):
        host_list.append(str(ip_address(begin_ip) + i))

    return host_ping(host_list)


if __name__ == '__main__':
    host_range_ping()
