# 南京大学每日健康填报自动打卡（适用青龙面板）

## 使用指南
### 添加依赖
在依赖管理-Linux添加gcc、g++依赖，然后在依赖管理-Python3添加requests、pycryptodome、pycryptodomex依赖

### 拉取脚本
`ql raw https://raw.githubusercontent.com/MilesPoupart/NjuHealthReport-qinglong/master/nju_health_report.py`

### 设置定时
手动设置定时即可

### 添加环境变量
1. nju_data（必填）：格式为学号\*&\*明文密码，如MG21000000\*&\*password
2. nju_report_enddate（可选）：在此日期前自动填报，格式为2022-12-31，不填默认打卡
3. nju_report_delay（可选）：触发任务后的延迟上下限，格式为延时下限&延时上限（秒），默认为10&60即延时10s-60s

### 微信/电报通知
只要在config.sh中配置好了通知设置，就可以自动通知

## 鸣谢
@zhangt2333 的原项目https://github.com/zhangt2333/actions-NjuHealthReport
