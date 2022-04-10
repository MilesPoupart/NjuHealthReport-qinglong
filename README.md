# 南京大学每日健康填报自动打卡（适用青龙面板）

请注意，2022年4月10日更新后，会强制获取前一天关于近期是否离宁和最近核酸日期的结果，并进行填报。

如果近期离宁情况更新或新做核酸检测，请务必手动填报一次！

如果APP界面中没有离宁情况和核酸检测的填报项，请停留在62dc0f6这一commit，不要更新！！！

## 使用指南
### 在docker中安装部署青龙面板
详见https://github.com/whyour/qinglong

openwrt系统若已内置docker，可在拉取whyour/qinglong:latest镜像后，使用以下代码创建容器：
```
docker run -dit \
   -v $PWD/ql/config:/ql/data/config \
   -v $PWD/ql/log:/ql/data/log \
   -v $PWD/ql/db:/ql/data/db \
   --net host \
   --name qinglong \
   --hostname qinglong \
   --restart always \
   whyour/qinglong:latest
```
青龙版本<=2.11请使用以下代码：
```
docker run -dit \
   -v $PWD/ql/config:/ql/config \
   -v $PWD/ql/log:/ql/log \
   -v $PWD/ql/db:/ql/db \
   --net host \
   --name qinglong \
   --hostname qinglong \
   --restart always \
   whyour/qinglong:latest
```

随后，通过http://\<ip\>:5700登录面板进行配置。

更多命令可参见[青龙项目指南](https://t.me/jiao_long/31)

### 添加依赖
在依赖管理-Linux添加gcc、g++依赖，然后在依赖管理-Python3添加requests、pycryptodome、pycryptodomex依赖

### 拉取脚本
```
ql raw https://raw.githubusercontent.com/MilesPoupart/NjuHealthReport-qinglong/master/nju_health_report.py
```

### 添加环境变量
1. nju_data（必填）：格式为`学号*&*明文密码`，如`MG21000000*&*password`，多账号请用"@&@"分割，如`MG21000000*&*password1@&@MG21000001*&*password2`
2. nju_report_enddate（可选）：在此日期前自动填报，格式为`2022-12-31`，不填默认打卡
3. nju_report_delay（可选）：触发任务后的延迟上下限，格式为延时下限&延时上限（秒），默认为`0&1500`即延时0s-1500s，请注意青龙面板配置文件config.sh中设置的单任务最大运行时间CommandTimeoutTime，以免运行时间过长被强制结束。

### 微信/电报通知
只要在config.sh中配置好了通知设置，就可以自动通知

### 设置定时
已默认设置定时为16 8,16,21 * * *，即每天8:16、16:16、21:16自动触发任务，如有需要，可手动修改。

## 已知问题
目前如果填报失败程序会出错退出，无法进行推送通知，已排查到与Exception相关，正在fix中。

## 鸣谢
@whyour 的青龙面板项目 https://github.com/whyour/qinglong

@zhangt2333 的原项目 https://github.com/zhangt2333/actions-NjuHealthReport
