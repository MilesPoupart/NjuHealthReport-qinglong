# -*- coding:utf-8 -*-
"""
cron: 16 8,16,21 * * *
new Env('南京大学每日健康自动填报');
"""
from Cryptodome.Cipher import AES
import base64
import json
import re
import sys
import logging
import time
import datetime
import os
import random
import requests


# from utils.py
def get_GMT8_timestamp():
    return (datetime.datetime.utcfromtimestamp((time.time())) + datetime.timedelta(hours=8)).timestamp()


def get_GMT8_str(format: str):
    return (datetime.datetime.utcfromtimestamp((time.time())) + datetime.timedelta(hours=8)).strftime(format)


def str_to_timestamp(time_str: str, format: str):
    return int(time.mktime(time.strptime(time_str, format)))


# notify service

def printT(s):
    print("[{0}]: {1}".format(
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), s))
    sys.stdout.flush()


class msg(object):
    def __init__(self, m=''):
        self.str_msg = m
        self.message()

    def message(self):
        global msg_info
        printT(self.str_msg)
        try:
            msg_info = "{}\n{}".format(msg_info, self.str_msg)
        except:
            msg_info = "{}".format(self.str_msg)
        sys.stdout.flush()  # 这代码的作用就是刷新缓冲区。
        # 当我们打印一些字符时，并不是调用print函数后就立即打印的。一般会先将字符送到缓冲区，然后再打印。
        # 这就存在一个问题，如果你想等时间间隔的打印一些字符，但由于缓冲区没满，不会打印。就需要采取一些手段。如每次打印后强行刷新缓冲区。

    def getsendNotify(self, a=0):
        if a == 0:
            a += 1
        try:
            url = 'https://gitee.com/curtinlv/Public/raw/master/sendNotify.py'
            response = requests.get(url)
            # msg("Downloading...")
            if 'curtinlv' in response.text:
                with open('sendNotify.py', "w+", encoding="utf-8") as f:
                    f.write(response.text)
            else:
                if a < 5:
                    a += 1
                    return self.getsendNotify(a)
                else:
                    pass
        except:
            if a < 5:
                a += 1
                return self.getsendNotify(a)
            else:
                pass

    def main(self):
        global send
        cur_path = os.path.abspath(os.path.dirname(__file__))
        sys.path.append(cur_path)
        if os.path.exists(cur_path + "/sendNotify.py"):
            try:
                from sendNotify import send
            except:
                self.getsendNotify()
                try:
                    from sendNotify import send
                except:
                    printT("加载通知服务失败~")
        else:
            self.getsendNotify()
            try:
                from sendNotify import send
            except:
                printT("加载通知服务失败~")


        ###################
msg().main()

# login service


def password_encrypt(text: str, key: str):
    """translate from encrypt.js"""
    def _rds(length): return ''.join([random.choice(
        'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678') for _ in range(length)])
    def pad(s): return s + (len(key) - len(s) %
                            len(key)) * chr(len(key) - len(s) % len(key))
    text = pad(_rds(64) + text).encode("utf-8")
    aes = AES.new(str.encode(key), AES.MODE_CBC, str.encode(_rds(16)))
    return str(base64.b64encode(aes.encrypt(text)), 'utf-8')


# example: login(username='your-student-id', password='your-password', to_url='https://ehall.nju.edu.cn:443/login?service=https://ehall.nju.edu.cn/ywtb-portal/official/index.html')
def login(username, password, to_url):
    """登录并返回JSESSIONID"""
    url = 'https://authserver.nju.edu.cn/authserver/login?service=' + to_url
    lt, dllt, execution, _eventId, rmShown, pwdDefaultEncryptSalt, cookies = getLoginCasData(
        url)
    data = dict(
        username=username,
        password=password_encrypt(password, pwdDefaultEncryptSalt),
        lt=lt,
        dllt=dllt,
        execution=execution,
        _eventId=_eventId,
        rmShown=rmShown,
    )
    try:
        response = requests.post(
            url=url,
            headers=HEADERS_LOGIN,
            data=data,
            cookies=cookies,
        )
        for resp in response.history:
            if resp.cookies.get('MOD_AUTH_CAS'):
                return resp.cookies
        if response.cookies.get('JSESSIONID'):
            return response.cookies
        raise Exception("login error")
    except execution as e:
        raise e


def getLoginCasData(url):
    """返回CAS数据和初始JSESSIONID"""
    try:
        response = requests.get(
            url=url,
            headers=HEADERS_LOGIN
        )
        if response.status_code == 200:
            # 获取 html 中 hidden 的表单 input
            lt = re.findall('name="lt" value="(.*?)"', response.text)[1]
            dllt = re.findall('name="dllt" value="(.*?)"', response.text)[1]
            execution = re.findall(
                'name="execution" value="(.*?)"', response.text)[1]
            _eventId = re.findall(
                'name="_eventId" value="(.*?)"', response.text)[1]
            rmShown = re.findall(
                'name="rmShown" value="(.*?)"', response.text)[1]
            pwdDefaultEncryptSalt = re.findall(
                'id="pwdDefaultEncryptSalt" value="(.*?)"', response.text)[0]
            return lt, dllt, execution, _eventId, rmShown, pwdDefaultEncryptSalt, response.cookies
    except Exception as e:
        raise e


HEADERS_LOGIN = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29",
}

# spider service


def get_apply_list(cookies):
    try:
        response = requests.get(
            url='http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/getApplyInfoList.do',
            headers=req_headers,
            cookies=cookies
        )
        data = json.loads(response.text)
        return data['data']
    except Exception as e:
        logging.exception(e)
        raise e


def do_apply(cookies, WID, location,leave_nanjing,last_test_time):
    try:
        response = requests.get(
            url='http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/saveApplyInfos.do',
            params=dict(
                WID=WID,
                IS_TWZC=1,
                IS_HAS_JKQK=1,
                JRSKMYS=1,
                JZRJRSKMYS=1,
                CURR_LOCATION=location,
                SFZJLN=leave_nanjing,
                ZJHSJCSJ=last_test_time
            ),
            headers=req_headers,
            cookies=cookies
        )
        if not (response.status_code == 200 and '成功' in response.text):
            raise Exception('健康填报失败')
        logging.info("填报成功")
    except Exception as e:
        logging.exception(e)
        raise e


def spidermain(username, password):
    # 登录
    cookies = login(username, password,
                    'http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/getApplyInfoList.do')
    # 获取填报列表
    apply_list = get_apply_list(cookies)
    if not apply_list[0]['TBRQ'] == get_GMT8_str('%Y-%m-%d'):
        raise Exception("当日健康填报未发布")
    try:
        if apply_list[0].get('CURR_LOCATION') is not None:
            location = apply_list[0].get('CURR_LOCATION')
        elif apply_list[1].get('CURR_LOCATION') is not None:
            location = apply_list[1].get('CURR_LOCATION')
        
        if apply_list[0].get('SFZJLN') is not None:
            leave_nanjing = apply_list[0].get('SFZJLN')
        elif apply_list[1].get('SFZJLN') is not None:
            leave_nanjing = apply_list[1].get('SFZJLN')
        
        if apply_list[0].get('ZJHSJCSJ') is not None:
            last_test_time = apply_list[0].get('ZJHSJCSJ')
        elif apply_list[1].get('ZJHSJCSJ') is not None:
            last_test_time = apply_list[1].get('ZJHSJCSJ')
    except Exception as e:
        logging.exception(e, '取昨日信息错误, 请手动在App填报一次')
        raise e
    # 填报当天
    msg("填报位置：%s" %location)
    msg("近期是否离开南京（1-是 0-否）：%s" %leave_nanjing)
    msg("上次核酸检测时间：%s" %last_test_time)
    do_apply(cookies, apply_list[0]['WID'], location,leave_nanjing,last_test_time)


req_headers = {
    "Host": "ehallapp.nju.edu.cn",
    "Connection": "keep-alive",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; NOH-AN00 Build/HUAWEINOH-AN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/88.0.4324.93 Mobile Safari/537.36 cpdaily/9.0.15 wisedu/9.0.15",
    "Referer": "http://ehallapp.nju.edu.cn/xgfw/sys/mrjkdkappnju/index.html",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en-CN;q=0.8,en;q=0.7,zh-HK;q=0.6,en-US;q=0.5",
    "X-Requested-With": "com.wisedu.cpdaily.nju",
}

if __name__ == '__main__':
    printT("南京大学每日健康自动填报")
    config_data = {}
    if "nju_data" in os.environ and os.environ["nju_data"]:
        config_data['userinfo'] = os.environ["nju_data"].split("@&@")
    else:
        msg("未设置nju_data环境变量！")
        send("南京大学每日健康自动填报", msg_info)
        exit(-1)
    if "nju_report_enddate" in os.environ and os.environ["nju_report_enddate"]:
        config_data['deadline'] = os.environ["nju_report_enddate"]
    else:
        msg("未设置nju_report_enddate环境变量！将默认打卡")
        config_data['deadline'] = '2099-12-31'

    if "nju_report_delay" in os.environ and os.environ["nju_report_delay"]:
        nju_report_delay = os.environ["nju_report_delay"].split("&")
        config_data['delay_min'] = int(nju_report_delay[0])
        config_data['delay_max'] = int(nju_report_delay[1])
    else:
        msg("未设置nju_report_delay环境变量！将启用默认0s-1500s延迟")
        config_data['delay_min'] = 0
        config_data['delay_max'] = 1500

    if get_GMT8_timestamp() > str_to_timestamp(config_data['deadline'], '%Y-%m-%d'):
        msg("超出填报日期")
        send("南京大学每日健康自动填报", msg_info)
        exit(-1)
    # retry mechanism
    for each_user in config_data['userinfo']:
        now_user_info = each_user.split("*&*")
        for _ in range(5):
            try:
                random.seed(str(datetime.datetime.now()))
                sleep_time = random.randint(
                    config_data['delay_min'], config_data['delay_max'])
                msg("任务触发时间 (GMT+8): " + get_GMT8_str('%Y-%m-%d %H:%M:%S'))
                msg("延时:" + str(sleep_time) + "秒")
                time.sleep(sleep_time)
                msg("开始打卡时间 (GMT+8): " + get_GMT8_str('%Y-%m-%d %H:%M:%S'))
                msg("南京大学每日健康自动填报：%s开始打卡！" % now_user_info[0])
                spidermain(now_user_info[0], now_user_info[1])
                msg("南京大学每日健康自动填报：%s填报成功！" % now_user_info[0])
                msg("如果14天内离开南京情况变化或新做核酸，请及时手动重新填报！")
                time.sleep(5)
                break
            except Exception as e:
                if _ == 4:
                    raise e
                msg("南京大学每日健康自动填报：填报失败，错误为%s" % str(e))
                logging.exception(e)
                time.sleep(5)
    send("南京大学每日健康自动填报", msg_info)
