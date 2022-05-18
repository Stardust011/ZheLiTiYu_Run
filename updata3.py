# coding:utf-8
import gzip
import hashlib
import random
import time
import requests
from geopy import distance

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


def betime():
    global nt
    t = ''
    ts = []
    print('e.g. 2022,2,17,17,3,38')
    t = input('time:')
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
    while line:
        l = line.split(' ')
        lonf.append(float(l[0]) + random.uniform(-0.00000500, 0.00000500) - 0.0065)  # bd坐标系偏移
        latf.append(float(l[1]) + random.uniform(-0.00000500, 0.00000500) - 0.0060)
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
    print(str((1000 / (dis / t)) / 60))
    if input('sure? press Enter for go on')!='':
       exit()
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
    getuid()
    betime()
    print('次数:')
    times = int(input())
    ic = 0
    nt = nt - 86400 * times
    timeArray = time.localtime(nt)
    print(time.strftime("%Y-%m-%d %H:%M:%S",timeArray))
    while ic < times:
        gps()
        ctime()
        crcon()
        post()
        check()
        nt = nt + 86400 + random.randint(-3600,3600)
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
