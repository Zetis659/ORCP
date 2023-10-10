import sys
import os
import requests
import time
import fake_useragent as fua
from user_agents import parse
import random as rnd

sys.path.append(os.path.join("home", "zetis", "Документы", "VScode", "ORCP"))


start = time.time()
black_list_mobile = ["smartphone", "iphone", "ipad", "ipod", "windows ce", "htc"]

while True:
    user = fua.UserAgent().random
    user_agent_check_mobile = parse(user)
    bl_check = False
    for word in black_list_mobile:
        if word in user.lower():
            bl_check = True
            break
    if not user_agent_check_mobile.is_mobile and not bl_check:
        break

random_port = rnd.randint(9050, 9149)
tor = f"socks5://127.0.0.1:{random_port}"
proxy = {"https": tor}

url = "https://auto.ru/-/ajax/desktop/listing/"
brands_list = []
params = {
    "category": "cars",
    "section": "all",
    "page": 1,
    "geo_id": [225],
    "sort": "cr_date-desc",
}

header = """
Host: auto.ru
User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0
Accept: */*
Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate, br
Referer: https://auto.ru/cars/haval/jolion/all/?page=2
x-client-app-version: 496.0.12587834
x-client-date: 1696585445030
x-csrf-token: ae0769f938ff7e60f9ebb5d18572daca6eeff242665a3778
x-requested-with: XMLHttpRequest
x-page-request-id: 21d65e742dba8c323bd67fa1dbb57624
x-retpath-y: https://auto.ru/cars/haval/jolion/all/?page=2
x-yafp: {"a1":"xM7YWvoLOdSDdA==;0","a2":";1","a3":"NvN3vuE6I2TbyDJwoUVpZg==;2","a4":"6SEq0cRwp/6DZS3byStGqL88DSIKnR7W1QvwtkgDYNApJQ==;3","a5":"B5sdXg2p2O5gYg==;4","a6":"m+4=;5","a7":"3tpdyVUOT3Ting==;6","a8":"KPQxoOMTN/g=;7","a9":"T7il30+CLgQfGQ==;8","b1":"0WInnaV7VmGI1g==;9","b2":"EQEQsEnwBWIaEA==;10","b3":"VRimEJSQGDpGAA==;11","b4":"rDYK1d2BNwY=;12","b5":"dTHdHtOLFvrUnw==;13","b6":"/MMo5vAwyZg=;14","b7":"AenSPZTgvL81qQ==;15","b8":"gs0fwDZfNhmuwQ==;16","b9":"/q41lUz1aReOrQ==;17","c1":"7e1pkA==;18","c2":"3Yw1zyz+SgZLjzdIYVeTSwYE;19","c3":"SuI9M3MB;20","c4":"lA93hJa2JlA=;21","c5":"uG12yZlh61k=;22","c6":"19XEKQ==;23","c7":"fDdO9uehAiA=;24","c8":"PJQLXtk47dk=;25","c9":"Y5ps88wkDQo=;26","d1":"BZYhw5hoOcmWVyb7ZfsoEbn773Ju3a7c;27","d2":"Vc8=;28","d3":"H93us5d/8d1y4Q==;29","d4":"P4MchPxIWDk=;30","d5":"qSkHnLvXSNDv5Q==;31","d7":"YfA=;32","d8":"/1cxObPTn/e4GbYnZkmlAC2T1i/HIUkaq+M=;33","d9":"DM9vjPPon4Y=;34","e1":"BQYPeKQo2O66VQ==;35","e2":"pXFLRLaWThyeSw==;36","e3":"Ia15zx8u2Bhnyg==;37","e4":"2qOVdvhp/Cw=;38","e5":"CYonz6sMc+Q54w==;39","e6":"2VEAcVzUoog=;40","e7":"GAqPMGuXc8iaAA==;41","e8":"NYnn1H3ZZehKTA==;42","e9":"eib0TJKAkYU=;43","f1":"6s+Pxlwyc6Du/Q==;44","f2":"FsaNQ7kZ87w=;45","f3":"8dA407aRSX/r5g==;46","f4":"L2OLeuR4pic=;47","f5":"xySriGTDtR0JsQ==;48","f6":"vlYIFxVrDxwACw==;49","f7":"qcskuwFpwcqDHw==;50","f8":"gWcSR8DVJv2gYg==;51","f9":"LtnitxgZB4M=;52","g1":"tERPkosqDI0=;53","g2":"crS55qaZl/wLdQ==;54","g3":"8ST4UAQt76DtSw==;55","g4":"K9/Eb75cGq3Dig==;56","g5":"8vzzNfovuCw=;57","g6":"MWVK+FRax1QV7w==;58","g7":"rNaCVc/iwcI=;59","g8":"K2Uu+StpPHA=;60","g9":"+cBsv7iInF8=;61","h1":"EQdCXb2HeNqZ6A==;62","h2":"JUiCvc7UkEBp7g==;63","h3":"VD4P/cTt4IIvIQ==;64","h4":"7HmSVYIJqgKxVQ==;65","h5":"O1nGrY+q1oA=;66","h6":"FlLRxZd8yfvSfg==;67","h7":"i1gAo/UzfRO3QBYFvIV4uQ4d3C0E8elniZq9C+sKUg8mcWNggXQUGB/x5aL07jg4SdL1N/6m6J+njM25wDQ/sZJYDKP/Mw==;68","h8":"PCZP0crghQsKlw==;69","h9":"nbwgw9M8x+Zg6Q==;70","i1":"4h1i75oPaeU=;71","i2":"FEphFjByqmjyMw==;72","i3":"DyZj4VxMaJJC0Q==;73","i4":"3/KmVmxrcV+ebg==;74","i5":"1E2zjvI5H2yNug==;75","z1":"4HGu7sFlpdKe36h791pKG5tdsFvl6S28P7kc/DPPLYR5kmjbB2PRaGgxVMXxdJJqu5jKRHj1gcxVdzGJZXYF8A==;76","z2":"zzBbZwlIqEg+MDICy7S+ubKv5twRNYHf0SwpZc6VnEM=;77","z3":"B1G+W5ROvbe8bg==;78","z6":"uoymE21MxHrRLc+o;79","z7":"E+/w1hw1qJzbmszf;80","z8":"WP+oVyWvThDAdA==;81","z9":"bbIDWerLq5ZcKw==;82","y1":"8DVXIoJas/4XrA==;83","y2":"2L6XhwuFRWD2Qg==;84","y3":"7ZDP5B/7tRbpfg==;85","y4":"0IcuG9+7FdRlFw==;86","y5":"Ls04/+eQnNTGmw==;87","y6":"XC6eBamizlCHww==;88","y7":"sHdC9XpAV3eH/lB5;89","y8":"9CtF87xYaWbT0Q==;90","y9":"sFlq7w93903hWw==;91","y10":"WLZJyGcyECU+6Q==;92","x1":"KPiOfR3dGlv5iQ==;93","x2":"o2YOQ4KKg4KCDQ==;94","x3":"ifP/WTbSM4ZWrw==;95","x4":"uDZKKQw4cPYPmg==;96","x5":"mmq4Gtwrjnst3OwX;97","z5":"EgS9agk+/vkinQ==;98","z4":"bMLtyNTpGW9OYDY9fSs=;99","v":"6.3.1","pgrdt":"qAXLk+MtJ3icW51yrnA1/KvygWo=;100","pgrd":"UydFVMtuDL2ww4DHjZraN9UTlgAwrdh4/Y3eqf0T0XDgS1LoaTqggKx7G9JIJ+n1y5WlQJjbjZKLKDGFSw4vowIhouaVP69X7yx2jmIjEEQ2+J+l0YHWOB+GAr5DuNSPtwkOXZxNA019s1P11MlEiP/O6E40ncv0dZcPwQO65UqNh0Cn8LvHr7YTMa7czeqObJAMDr2Po/hdvPX8RUO7YzDKFO8="}
content-type: application/json
Origin: https://auto.ru
Content-Length: 109
Connection: keep-alive
Cookie: _yasc=gZQeDSB8+mTj40NG48GLbxjfHWbmcw/xDM+JwnKUf2lYOy1FEcqhAiJvtSpyx1DeUDbr; autoru_gdpr=1; suid=1207517205cbc001df37a30ed79f5093.0cab0997bb14038e58807e6541a9931d; _csrf_token=ae0769f938ff7e60f9ebb5d18572daca6eeff242665a3778; autoru_sid=37476463%7C1696585348812.7776000.zIOnkbKwVJXK-47SOs7ebQ.3mCbC7SY1B7bZbqrjLQrdeGBdK3e_OZ7q8n0l7etXT8; autoruuid=g651fd6652490scfcsk1m72tvi0mifna.613aeb41efcdff059dcda0fbe9b67d38; from_lifetime=1696585434233; from=direct; autoru_sso_blocked=1; Session_id=noauth:1696585318; sessar=1.1182.CiAQwsfqKTZFzckJxhxHbtokSL8fOpElpAe_adCPEBTzeQ.MYWupd2uowDyF3ukE2nNYrXKfSmHrN7c0Z09ZowlrKo; yandex_login=; ys=c_chck.2776547506; i=liHN55+7CmGEO0ipWeTpn6+g8SOZnhyVUyxBA1oW6MTJ8rBDbEu0flqO5UE1r7wOjOmG2cbum4IXRt+Y+GPL/VDDxKM=; yandexuid=1924770611696585318; mda2_beacon=1696585318208; sso_status=sso.passport.yandex.ru:synchronized_no_beacon; counter_ga_all7=2; layout-config={"screen_height":600,"screen_width":1800,"win_width":1800,"win_height":600}; fp=b37fee826d91e67f9d347a1d37774de6%7C1696585325711; count-visits=4; yaPassportTryAutologin=1; popups-dr-shown-count=1; cycada=8EaJOFKZ47IvDP+Bk1s2/CEzo0pzLACKgBN0JiaWT4A=
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: same-origin
Sec-Fetch-Site: same-origin
TE: trailers
"""

headers = header.strip().split("\n")

dict_headers = {}

for header in headers:
    key, value = header.split(": ")
    dict_headers[key] = value
(dict_headers["User-Agent"]) = user

if __name__ == "__main__":
    response = requests.post(url, json=params, headers=dict_headers, proxies=proxy)
    print(response.status_code)
    data = response.json()
    try:
        if data["type"] == "captcha":
            print("CAPTCHA!")
    except:
        print(f"JSON DATA: {data}\n\nThe header is set correctly!!!")
        
