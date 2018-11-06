# !/user/bin/env python
# -*- coding:utf-8 -*- 
# time: 2018/11/4--17:59
__author__ = 'Henry'

import hashlib,json,time,base64,requests
from Spiders.AES import AES_encrypt,AES_decrypt,AES_encrypt_history,AES_decrypt_history
from Spiders.DES import DES_decrypt,DES_decrypt_history


# 天气数据详细网址: https://www.aqistudy.cn/html/city_detail.html
def get_aqistudy(method,city,type,startTime,endTime):
    '''
    按小时/日/月查询
    :param method: 查询数据方法 (1."GETDETAIL"-详情数据:time,aqi,pm2_5,pm10,co,no2,o3,so2,rank;2."GETCITYWEATHER"-天气数据:time,temp,humi,wse,wd,tq)
    :param city: 查询城市 (eg:"北京")
    :param type: 查询时间类型三种(时HOUR/日DAY/月MONTH)
    :param startTime: 起始时间 (eg:"2018-11-03 10:00:00")
    :param endTime: 结束时间 (eg:"2018-11-03 13:00:00")
    :returns weather_data: 天气数据
    '''

    # Step1:加密提交参数
    queryparam = {
        'city':city, # 城市
        'endTime':endTime, # 结束时间
        'startTime':startTime, # 起始时间
        'type':type # 查询时间类型3种: 时(HOUR)/日(DAY)/月(MONTH)
      }
    appId = '1a45f75b824b2dc628d5955356b5ef18'
    clienttype = 'WEB'
    timestamp = str(int(time.time()*1000))
    json_2 = json.dumps(queryparam).encode('utf-8').decode('unicode_escape').replace(': ',':').replace(', ',',')
    param = {
        'appId':appId,
        'method':method,
        'timestamp':int(timestamp),
        'clienttype':clienttype,
        'object':queryparam,
        'secret': hashlib.md5((appId + method + timestamp + clienttype + json_2).encode()).hexdigest()
    }
    json_3 = json.dumps(param).encode('utf-8').decode('unicode_escape').replace(': ',':').replace(', ',',').encode()
    param = base64.b64encode(json_3).decode()
    aes_encrypted = AES_encrypt(param)
    url = 'https://www.aqistudy.cn/apinew/aqistudyapi.php'
    data = {'d':aes_encrypted}
    headers = {
        'Host':'www.aqistudy.cn',
        'Origin':'https://www.aqistudy.cn',
        'Referer':'https://www.aqistudy.cn/html/city_detail.html',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    html = requests.post(url,data=data,headers=headers)
    encrypted_data = html.text

    # Step2:解密返回的加密数据
    '''
    解密函数:
    function decodeData(data) {
    data = AES.decrypt(data, aes_server_key, aes_server_iv);
    data = DES.decrypt(data, des_key, des_iv);
    data = BASE64.decrypt(data);
    return data
    }
    '''
    aes_decrypted = AES_decrypt(encrypted_data)
    des_decrypted = DES_decrypt(aes_decrypted)
    weather_data = base64.b64decode(des_decrypted).decode()
    print(weather_data)
    # Step3:解析天气数据
    data = json.loads(weather_data)
    if data.get('success') == True and data.get('errcode') == 0:
        print('恭喜您,查询天气数据成功!')
        data = data.get('result').get('data')
        total = data.get('total')
        print('一共查询到{}组数据:'.format(total))
        for i in data.get('rows'):
            print(i)
    else:
        print('抱歉,查询天气数据失败!请核对查询参数是否正确!')


# 历史数据查询网址: https://www.aqistudy.cn/historydata/monthdata.php?city=%E5%8C%97%E4%BA%AC
def get_history(city,month):
    '''
    按月查询每天的历史数据
    :param city: 查询城市 (eg:"北京")
    :param month: 查询月份(eg:"201811"; 即查询2018年11月每天的数据)
    :returns weather_data: 天气数据
    '''

    # Step1:加密提交参数
    # 查询数据方法
    method = "GETDAYDATA"
    queryparam = {
        'city':city, # 城市 eg: "北京"
        'month':month # 只能按月查询 eg: "201811"
      }
    # (1)Base64加密
    appId = 'b73a4aaa989f54997ef7b9c42b6b4b29'
    clienttype = 'WEB'
    timestamp = str(int(time.time()*1000))
    json_2 = json.dumps(queryparam).encode('utf-8').decode('unicode_escape').replace(': ',':').replace(', ',',')
    param = {
        'appId':appId,
        'method':method,
        'timestamp':int(timestamp),
        'clienttype':clienttype,
        'object':queryparam,
        'secret': hashlib.md5((appId + method + timestamp + clienttype + json_2).encode()).hexdigest()
    }
    json_3 = json.dumps(param).encode('utf-8').decode('unicode_escape').replace(': ',':').replace(', ',',').encode()
    param = base64.b64encode(json_3).decode()
    aes_encrypted = AES_encrypt_history(param)
    url = 'https://www.aqistudy.cn/historydata/api/historyapi.php'
    data = {'hd':aes_encrypted}
    headers = {
        'Host':'www.aqistudy.cn',
        'Origin':'https://www.aqistudy.cn',
        'Referer':'https://www.aqistudy.cn/html/city_detail.html',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    html = requests.post(url,data=data,headers=headers)
    encrypted_data = html.text
    # print('返回加密数据:' + encrypted_data)
    # Step2:解密返回的加密数据
    '''
    解密函数:
    function decodeData(data) {
    data = BASE64.decrypt(data);
    data = DES.decrypt(data, des_key, des_iv);
    data = AES.decrypt(data, aes_server_key, aes_server_iv);
    data = BASE64.decrypt(data);
    return data
    }
    '''
    base64_decrypted = base64.b64decode(encrypted_data).decode()
    des_decrypted = DES_decrypt_history(base64_decrypted).decode()
    aes_decrypted = AES_decrypt_history(des_decrypted)
    weather_data = base64.b64decode(aes_decrypted).decode()
    print(weather_data)
    # Step3:解析天气数据
    data = json.loads(weather_data)
    if data.get('success') == True and data.get('errcode') == 0:
        print('恭喜您,查询天气数据成功!')
        data = data.get('result').get('data')
        total = data.get('num')
        print('一共查询到{}组数据:'.format(total))
        for i in data.get('items'):
            print(i)
    else:
        print('抱歉,查询天气数据失败!请核对查询参数是否正确!')


if __name__ == '__main__':
    # 三种查询方式
    get_aqistudy('GETDETAIL', '上海', 'HOUR', '2018-11-06 05:00:00', '2018-11-06 08:00:00')
    get_aqistudy('GETCITYWEATHER', '上海', 'HOUR', '2018-11-06 05:00:00', '2018-11-06 08:00:00')
    get_history('上海', '201811')
