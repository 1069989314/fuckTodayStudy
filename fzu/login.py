# -*- coding: utf-8 -*-
import time
import requests
from utils import *

# 全局配置
config = getYmlConfig()
session = requests.session()
user = config['user']
# Cpdaily-Extension
extension = {
    "lon": user['lon'],
    "model": "PCRT00",
    "appVersion": "8.0.8",
    "systemVersion": "4.4.4",
    "userId": user['username'],
    "systemName": "android",
    "lat": user['lat'],
    "deviceId": str(uuid.uuid1())
}
CpdailyInfo = DESEncrypt(json.dumps(extension))
host = 'fzu.cpdaily.com'


# 获取验证码
def getMessageCode():
    log('正在获取验证码。。。')
    headers = {
        'SessionToken': 'szFn6zAbjjU=',
        'clientType': 'cpdaily_student',
        'tenantId': '',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.4; PCRT00 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Safari/537.36 okhttp/3.8.1',
        'deviceType': '1',
        'CpdailyStandAlone': '0',
        'CpdailyInfo': CpdailyInfo,
        'RetrofitHeader': '8.0.8',
        'Cache-Control': 'max-age=0',
        'Content-Type': 'application/json; charset=UTF-8',
        'Host': 'www.cpdaily.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
    }
    params = {
        'mobile': DESEncrypt(str(user['tellphone']))
    }
    url = 'https://www.cpdaily.com/v6/auth/authentication/mobile/messageCode'
    res = session.post(url=url, headers=headers, data=json.dumps(params))
    errMsg = res.json()['errMsg']
    if errMsg != None:
        log(errMsg)
        exit(-1)
    log('获取验证码成功。。。')


# 手机号登陆
def mobileLogin(code):
    log('正在验证验证码。。。')
    headers = {
        'SessionToken': 'szFn6zAbjjU=',
        'clientType': 'cpdaily_student',
        'tenantId': '',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.4; PCRT00 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Safari/537.36 okhttp/3.8.1',
        'deviceType': '1',
        'CpdailyStandAlone': '0',
        'CpdailyInfo': CpdailyInfo,
        'RetrofitHeader': '8.0.8',
        'Cache-Control': 'max-age=0',
        'Content-Type': 'application/json; charset=UTF-8',
        'Host': 'www.cpdaily.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
    }
    params = {
        'loginToken': str(code),
        'loginId': str(user['tellphone'])
    }
    url = 'https://www.cpdaily.com/v6/auth/authentication/mobileLogin'
    res = session.post(url=url, headers=headers, data=json.dumps(params))
    errMsg = res.json()['errMsg']
    if errMsg != None:
        log(errMsg)
        exit(-1)
    log('验证码验证成功。。。')
    return res.json()['data']


# 验证登陆信息
def validation(data):
    log('正在验证登陆信息。。。')
    sessionToken = data['sessionToken']
    tgc = data['tgc']
    headers = {
        'SessionToken': DESEncrypt(sessionToken),
        'clientType': 'cpdaily_student',
        'tenantId': 'fzu',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.4; PCRT00 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Safari/537.36 okhttp/3.8.1',
        'deviceType': '1',
        'CpdailyStandAlone': '0',
        'CpdailyInfo': CpdailyInfo,
        'RetrofitHeader': '8.0.8',
        'Cache-Control': 'max-age=0',
        'Content-Type': 'application/json; charset=UTF-8',
        'Host': 'www.cpdaily.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Cookie': 'sessionToken=' + sessionToken
    }
    params = {
        'tgc': DESEncrypt(tgc)
    }
    url = 'https://www.cpdaily.com/v6/auth/authentication/validation'
    res = session.post(url=url, headers=headers, data=json.dumps(params))
    errMsg = res.json()['errMsg']
    if errMsg != None:
        log(errMsg)
        exit(-1)
    log('验证登陆信息成功。。。')
    return res.json()['data']


# 更新acw_tc
def updateACwTc(data):
    log('正在更新acw_tc。。。')
    sessionToken = data['sessionToken']
    tgc = data['tgc']
    amp = {
        'AMP1': [{
            'value': sessionToken,
            'name': 'sessionToken'
        }],
        'AMP2': [{
            'value': sessionToken,
            'name': 'sessionToken'
        }]
    }
    headers = {
        'TGC': DESEncrypt(tgc),
        'AmpCookies': DESEncrypt(json.dumps(amp)),
        'SessionToken': DESEncrypt(sessionToken),
        'clientType': 'cpdaily_student',
        'tenantId': 'fzu',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.4; PCRT00 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Safari/537.36 okhttp/3.8.1',
        'deviceType': '1',
        'CpdailyStandAlone': '0',
        'CpdailyInfo': CpdailyInfo,
        'RetrofitHeader': '8.0.8',
        'Cache-Control': 'max-age=0',
        'Host': host,
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'
    }
    url = 'https://{host}/wec-portal-mobile/client/userStoreAppList'.format(host=host)
    # 清除cookies
    # session.cookies.clear()
    session.get(url=url, headers=headers, allow_redirects=False)
    log('更新acw_tc成功。。。')


# 获取MOD_AUTH_CAS
def getModAuthCas(data):
    log('正在获取MOD_AUTH_CAS。。。')
    sessionToken = data['sessionToken']
    headers = {
        'Host': host,
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.4; PCRT00 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Safari/537.36 cpdaily/8.0.8 wisedu/8.0.8',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'X-Requested-With': 'com.wisedu.cpdaily'
    }
    url = 'https://{host}/wec-counselor-collector-apps/stu/mobile/index.html?timestamp='.format(host=host) + str(
        int(round(time.time() * 1000)))
    res = session.get(url=url, headers=headers, allow_redirects=False)
    location = res.headers['location']
    # print(location)
    headers2 = {
        'Host': 'www.cpdaily.com',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.4; PCRT00 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Safari/537.36 cpdaily/8.0.8 wisedu/8.0.8',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'Cookie': 'clientType=cpdaily_student; tenantId=fzu; sessionToken=' + sessionToken,
    }
    res = session.get(url=location, headers=headers2, allow_redirects=False)
    location = res.headers['location']
    # print(location)
    session.get(url=location, headers=headers)
    cookies = requests.utils.dict_from_cookiejar(session.cookies)
    if 'MOD_AUTH_CAS' not in cookies:
        log('获取MOD_AUTH_CAS失败。。。')
        exit(-1)
    log('获取MOD_AUTH_CAS成功。。。')


# 通过手机号和验证码进行登陆
def login():
    # 1. 获取验证码
    getMessageCode()
    code = input("请输入验证码：")
    # 2. 手机号登陆
    data = mobileLogin(code)
    # 3. 验证登陆信息
    data = validation(data)
    # 4. 更新acw_tc
    updateACwTc(data)
    # 5. 获取mod_auth_cas
    getModAuthCas(data)
    print('==============sessionToken填写到index.py==============')
    sessionToken = data['sessionToken']
    print(sessionToken)
    print('==============CpdailyInfo填写到index.py==============')
    print(CpdailyInfo)
    print('==============Cookies填写到index.py==============')
    print(requests.utils.dict_from_cookiejar(session.cookies))


if __name__ == '__main__':
    login()
