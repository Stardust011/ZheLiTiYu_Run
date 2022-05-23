import hashlib
import random
import requests
from urllib.request import quote
import gzip

r = requests
学号 = input("学号：")
en_md5 = hashlib.md5()
en_md5.update(random.randbytes(64))
res = en_md5.hexdigest()
print(res)
headers = {"Charset": "UTF-8","User-Agent": "Dalvik/2.1.0 (Linux; U; Android ; M2011K2C Build/RKQ1.200928.002)"}
str3 = ""
str3 = "['bangdingschool','10338" + "','" + 学号 + "','" + res + "','vivo','V21312','andriod','"+ str(random.randint(10,12)) + "']"
url3 = "http://quantiwang.cn:8012/cloud/DflyServer"
print(quote(str3))
pay_loads3 = ""
pay_loads3 = {'name' : str3}
r3 = r.post(url=url3,data=pay_loads3,headers=headers)
print(r3.text)
r3_l = r3.text.split(',')
print(r3_l[0])
uid = r3_l[2]

url = r'http://10.11.246.182:8029/DragonFlyServ/Api/webserver/getRunDataSummary'
data = {'studentno': 学号,
        'uid': uid}
f_out = gzip.compress(str(data).encode('utf-8'))
requ = requests.post(url=url, headers=headers, data=f_out)
print(requ.text)