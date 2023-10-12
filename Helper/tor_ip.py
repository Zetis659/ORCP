import requests
import random as rnd

random_port = rnd.randint(9050, 9149)
proxy_tor = f'socks5://127.0.0.1:{random_port}'
optional_proxy = {'https':proxy_tor}
link = 'https://api.ipify.org'
res = requests.get(link, proxies=optional_proxy).text

print(f'Ваш IP: {res}')
