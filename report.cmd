@REM set http_proxy=http://127.0.0.1:7890
@REM set https_proxy=http://127.0.0.1:7890
set nju_data=MG21000000*^&*password
@REM set nju_report_delay=0^&1500
@REM set nju_report_enddate=2023-12-31
@REM 以Telegram为例，其他通知变量请参考report.sh
set TG_BOT_TOKEN=19xxxxxx:xxxxxxxxxxxxxxxxx
set TG_USER_ID=19xxxxxxx
python nju_health_report.py