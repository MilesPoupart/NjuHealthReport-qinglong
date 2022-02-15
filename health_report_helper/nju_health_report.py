# -*- coding: utf-8 -*-
#!/usr/bin/env python
# Copyright 2021 zhangt2333. All Rights Reserved.
# Author-Github: github.com/zhangt2333
# main.py 2021/9/11 13:01
import json
import re
import sys
import logging
import time,datetime
import os
import random

import config
import spider
import utils

def printT(s):
    print("[{0}]: {1}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), s))
    sys.stdout.flush()

## 获取通知服务
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
        sys.stdout.flush()           #这代码的作用就是刷新缓冲区。
                                     # 当我们打印一些字符时，并不是调用print函数后就立即打印的。一般会先将字符送到缓冲区，然后再打印。
                                     # 这就存在一个问题，如果你想等时间间隔的打印一些字符，但由于缓冲区没满，不会打印。就需要采取一些手段。如每次打印后强行刷新缓冲区。
    def getsendNotify(self, a=0):
        if a == 0:
            a += 1
        try:
            url = 'https://gitee.com/curtinlv/Public/raw/master/sendNotify.py'
            response = requests.get(url)
            msg("Downloading...")
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

if __name__ == '__main__':
    printT("南京大学每日健康自动填报")
    if len(sys.argv) > 1:
        config.data = json.loads(re.sub('#(.*)\n', '\n', sys.argv[1]).replace("'", '"'))
    if utils.get_GMT8_timestamp() > utils.str_to_timestamp(config.data['deadline'], '%Y-%m-%d'):
        msg("超出填报日期")
        send("南京大学每日健康自动填报",msg_info)
        exit(-1)
    # retry mechanism
    for _ in range(5):
        try:
            random.seed(datetime.datetime.now())
            sleep_time = random.randint(5, 10)
            msg("任务触发时间 (GMT+8): " + utils.get_GMT8_str('%Y-%m-%d %H:%M:%S'))
            msg("延时:" + str(sleep_time) + "秒")
            time.sleep(sleep_time)
            msg("开始打卡时间 (GMT+8): " + utils.get_GMT8_str('%Y-%m-%d %H:%M:%S'))
            spider.main(config.data['username'], config.data['password'])
            msg("南京大学每日健康自动填报：填报成功！")
            break
        except Exception as e:
            if _ == 4:
                raise e
            send("南京大学每日健康自动填报：填报失败，错误为%s" %e)
            logging.exception(e)
            time.sleep(5)
    send("南京大学每日健康自动填报",msg_info)