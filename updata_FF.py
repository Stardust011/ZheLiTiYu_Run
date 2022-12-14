# coding:utf-8
import gzip
import hashlib
import random
import time
import requests
import math
from geopy import distance
import base64
from Crypto.Hash import SHA512
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import pyotp

totp = pyotp.totp.TOTP('vUwNiE3cxh4tiwRl74ly')
if not totp.verify(input('请输入动态验证码:')):
    print('错误')
    print('请联系管理员')
    print('EMAIL:lin.stardusts@gmail.com')
    input()
    exit(0)

dis = 0  # distance
t = 0  # all time
tc = []
cc = 0  # steps count
content = {}
nt = 0  # began time
lon = []
lat = []
latf = []
lonf = []
studentno = ''
uid = ''

def to_verify_with_public_key(signature, plain_text):
    with open('rsa-pub.pem', 'r') as f:
        public_key = f.read()
    #公钥验签
    verifier = PKCS1_v1_5.new(RSA.importKey(public_key))
    _rand_hash = SHA512.new()
    _rand_hash.update(plain_text.encode())
    verify = verifier.verify(_rand_hash, signature)
    return verify #true / false

def betime():
    global nt
    t = ''
    ts = []
    # print('e.g. 2022,2,17,17,3,38')
    # t = input('time:')
    t == ''
    if t == '':
        nt = int(time.time())
    else:
        t = t + ',23,2,5'
        tt = t.split(',')
        i = 0
        while i < len(tt):
            ts.append(int(tt[i]))
            i = i + 1
        nt = int(time.mktime(tuple(ts)))
    nt = nt - 25 * 60
    print('get time   ' + str(nt))
    return nt


def gps():
    global dis
    global latf
    global lonf
    global cc
    f = open('gps.txt')
    line = f.readline()
    l = []
    cc = 0
    Pi = math.pi * 3000.0 / 180.0
    while line:
        l = line.split(' ')
        # 开始处理bd坐标系偏移问题 bd09 --> GCJ02
        x = float(l[0]) + random.uniform(-0.00000500, 0.00000500) - 0.0065
        y = float(l[1]) + random.uniform(-0.00000500, 0.00000500) - 0.0060
        z = math.sqrt(pow(x, 2) + pow(y, 2)) - 0.00002 * math.sin(y * Pi)
        theta = math.atan2(y, x) - 0.000003 * math.cos(x * Pi)
        lonf.append(z * math.cos(theta))  
        latf.append(z * math.sin(theta))
        # 偏移完成
        line = f.readline()
        cc = cc + 1
    i = 1
    while i < cc:
        loc1 = (latf[i - 1], lonf[i - 1])
        loc2 = (latf[i], lonf[i])
        d = distance.distance(loc1, loc2).meters
        dis = dis + d
        i = i + 1
    f.close()
    print('get path')
    print(dis)


def ctime():
    global t
    global tc
    global nt
    i = 1
    while i <= cc:
        t1 = random.randint(-1, 1)
        t = t + 4 + t1
        tc.append(nt + 4 * i + t1)
        i = i + 1
    print(t)


def crcon():  # 校内定向跑
    global content
    global uid
    global studentno
    gpsd = []
    conpath = ['30.314971,120.350531', '30.313175,120.352765', '30.313372,120.355463', '30.312419,120.352006',
               '30.313407,120.350912']
    path = random.sample(conpath, 4)
    dpath = ','.join(path)
    print(dpath)
    i = 0
    line = ''
    while i < cc:
        line = str(latf[i]) + '0,' + str(lonf[i]) + '0;' + str(tc[i]) + ';null;null;' + str(
            round(random.uniform(2.5, 1.5), 1)) + ';null'
        gpsd.append(line)
        i = i + 1
    gdata = '@'.join(gpsd)
    content = {'begintime': str(nt), 'endtime': str(nt + t),
               'uid': uid,
               'schoolno': '10338', 'distance': str(round(dis, 1)), 'speed': str(dis / t) + "0",
               'studentno': studentno, 'atttype': '3', 'eventno': '800', 'location': gdata, 'pointstatus': '1',
               'usetime': str(t) + ".0", 'path': dpath}  # 需要path
    # 'path':'30.314971,120.350531;30.313175,120.352765;30.313372,120.355463;30.312419,120.352006;'
    # print(str((1000 / (dis / t)) / 60))
    # if input('sure? press Enter for go on')!='':
    #    exit()
    return (content)


def post():
    url = r'http://10.11.246.182:8029/DragonFlyServ/Api/webserver/uploadRunData'
    headers = {"Connection": "Keep-Alive", "Charset": "UTF-8",
               "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 12; M2011K2C Build/RKQ1.200928.002)",
               "Host": "10.11.246.182:8029"}
    f = str(content).encode('utf-8')
    d = gzip.compress(f)
    requ = requests.post(url, headers=headers, data=d)
    print(requ.text)


def check():
    global uid
    global studentno
    headers = {"Connection": "Keep-Alive", "Charset": "UTF-8",
               "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 12; M2011K2C Build/RKQ1.200928.002)",
               "Host": "10.11.246.182:8029"}
    url = r'http://10.11.246.182:8029/DragonFlyServ/Api/webserver/getRunDataSummary'
    data = {'studentno': studentno,
            'uid': uid}
    f_out = gzip.compress(str(data).encode('utf-8'))
    requ = requests.post(url=url, headers=headers, data=f_out)
    print(requ.text)

def getuid():
    global uid
    global studentno
    r = requests
    studentno = input("学号：")
    en_md5 = hashlib.md5()
    en_md5.update(random.randbytes(64))
    res = en_md5.hexdigest()
    headers = {"Charset": "UTF-8","User-Agent": "Dalvik/2.1.0 (Linux; U; Android ; M2011K2C Build/RKQ1.200928.002)"}
    str3 = ""
    str3 = "['bangdingschool','10338" + "','" + studentno + "','" + res + "','vivo','V21312','andriod','"+ str(random.randint(10,12)) + "']"
    url3 = "http://quantiwang.cn:8012/cloud/DflyServer"
    pay_loads3 = ""
    pay_loads3 = {'name' : str3}
    r3 = r.post(url=url3,data=pay_loads3,headers=headers)
    r3_l = r3.text.split(',')
    uid = r3_l[2]
    return 1

if __name__ == '__main__':
    with open('gps.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    with open('updata.py.sig', 'r') as f:
        signature = f.read()
    signature = base64.b64decode(signature)
    assert to_verify_with_public_key(signature, text)
    if int(time.time()) > 1671119999:
        print('时间到了，不再运行')
        input()
        exit()
    try:
        getuid()
        betime()
        print('公里数(3的整倍数,如120):')
        times = math.ceil(int(input())/3)
        ic = 0
        nt = nt - 86400 * times
        timeArray = time.localtime(nt)
        print(time.strftime("%Y-%m-%d %H:%M:%S",timeArray))
        while ic < times:
            gps()
            ctime()
            crcon()
            try:
                post()
                check()
            except:
                print("请确认已连接校园网")
                input()
            nt = nt + 86400 + random.randint(-1800,1800)
            timeArray = time.localtime(nt)
            print(time.strftime("%Y-%m-%d %H:%M:%S",timeArray))
            dis = 0
            t = 0  # all time
            tc = []
            cc = 0  # steps count
            content = {}
            lon = []
            lat = []
            latf = []
            lonf = []
            ic = ic + 1
    except:
        print("出现错误，请检测输入")
        input()
