"""
Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться
доступность сетевых узлов. Аргументом функции является список, в котором каждый
сетевой узел должен быть представлен именем хоста или ip-адресом. В функции
необходимо перебирать ip-адреса и проверять их доступность с выводом
соответствующего сообщения («Узел доступен», «Узел недоступен»).
При этом ip-адрес сетевого узла должен создаваться с помощью функции
ip_address().
"""

from ipaddress import ip_address
from subprocess import Popen, PIPE


def host_ping(list_ip_addresses, timeout=100, requests=1):
    results = {'Доступные': "", 'Недоступные': ""}
    for address in list_ip_addresses:
        try:
            address = ip_address(address)
        except ValueError:
            pass

        process = Popen(f"ping {address} -w {timeout} -n {requests}",
                        shell=False, stdout=PIPE)
        process.wait()

        if process.returncode == 0:
            results['Доступные'] += f"{str(address)}\n"
            res_string = f'{address} - Узел доступен'
        else:
            results['Недоступные'] += f"{str(address)}\n"
            res_string = f'{address} - Узел недоступен'
        print(res_string)
    return results


if __name__ == '__main__':
    ip_addresses = ['192.168.0.1', 'google.com', '192.168.0.40', 'wikipedia.com']
    host_ping(ip_addresses)
