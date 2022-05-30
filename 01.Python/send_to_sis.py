#! /usr/bin/python3
# _*_ coding:UTF-8 _*_

import json
import os
import re
import smtplib
import time
from email.header import Header
from email.mime.text import MIMEText

import requests

# avoid ssl error
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'

usr_input_code = ""
need_send_email = False
report_file_name = 'exec_result.html'


def write_exec_result_to_file(log_str):
    file = open(report_file_name, mode="a+", encoding="UTF-8")
    input_str = f"<br>{log_str}"
    file.write(input_str)


def write_message_header():
    m_time_stamp = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    tp_str = f"<br><br><br><br>the python exec at {m_time_stamp}<br>"
    r = requests.get("https://ip.gs/json")
    json_str = json.loads(r.text)
    print(json_str)

    tp_str = tp_str + f"IP信息如下:<br><br>IP:{json_str['ip']}<br>国家:{json_str['country']}<br>" \
                      f"区域:{json_str.get('region_name', None)}" \
                      f"<br>城市:{json_str.get('city', None)}<br>纬度:{json_str.get('latitude', None)}\t" \
                      f"经度:{json_str.get('longitude', None)}" \
                      f"<br>时区:{json_str['time_zone']}<br>asnOrg:{json_str.get('asn_org', None)}"
    write_exec_result_to_file(tp_str)


def send_email_with_smtp():
    # if not need_send_email:
    #   print("GitHub Action Python Script, Do not trigger Send Email Action")
    #  return
    # py3_env = os.environ['PYTHON3HOME']
    print(os.environ)
    email_config_server_domain = os.environ['EMAIL_SMTP_DOMAIN']
    # print(f"1:{email_config_server_domain}")
    email_config_server_port = os.environ['EMAIL_SMTP_PORT']
    # print(f'2{email_config_server_port}')
    email_config_server_user_name = os.environ['EMAIL_SMTP_USER_NAME']
    # print(f'3{email_config_server_user_name}')
    email_config_server_user_pwd = os.environ['EMAIL_SMTP_USER_PWD']
    # print(f'4{email_config_server_user_pwd}')
    email_config_server_recv_user_name = os.environ['EMAIL_SMTP_REV']
    # print(f'5{email_config_server_recv_user_name}')

    with open(report_file_name, 'r') as report_f:
        report_string = report_f.read()
    msg = MIMEText(report_string, 'plain', 'UTF-8')
    msg['From'] = f"杨总裁的小秘书"
    msg['To'] = f"{email_config_server_recv_user_name}"
    msg['Subject'] = Header("玲仔笑一笑，玲仔十年少", 'UTF-8').encode()
    # msg['From'] = formataddr(['smtp_python_user_name', f"{email_config_server_user_name}")
    # msg['To'] = Header(email_config_server_recv_user_name, 'UTF-8')
    # msg['Subject'] = Header('test python email module', 'UTF-8').encode()
    #
    smtp_obj = smtplib.SMTP_SSL(email_config_server_domain, int(email_config_server_port))
    # smtp_obj.set_debuglevel(1)
    smtp_obj.login(user=email_config_server_user_name, password=email_config_server_user_pwd)
    smtp_obj.sendmail(email_config_server_user_name, email_config_server_recv_user_name, msg.as_string())
    smtp_obj.quit()


def get_weather_info():
    # http://t.weather.itboy.net/api/weather/city/101230501 泉州天气
    url = "http://t.weather.itboy.net/api/weather/city/101230501"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/98.0.4758.102 Safari/537.36",
        "DNT": "1",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.gdlottery.cn/?v=1652849733245"
    }
    r = requests.get(url, headers=headers)
    print(r.text)
    weather_list = json.loads(r.text)
    tp_str = f"时间:{weather_list.get('time', 'None')}<br>" \
             f"当前城市:{weather_list['cityInfo']['parent']}  {weather_list['cityInfo']['city']}<br>"
    index = 0
    while index < 3:
        tp_str = tp_str + f"日期:{weather_list['data']['forecast'][index]['date']}--{weather_list['data']['forecast'][index]['week']}<br>" \
             f"天气:{weather_list['data']['forecast'][index]['type']}<br>" \
             f"{weather_list['data']['forecast'][index]['high']}<br>{weather_list['data']['forecast'][index]['low']}<br>" \
             f"日出时分:{weather_list['data']['forecast'][index]['sunrise']}<br>日落时分:{weather_list['data']['forecast'][index]['sunset']}<br>" \
             f"风向:{weather_list['data']['forecast'][index]['fx']}<br>风级:{weather_list['data']['forecast'][index]['fl']}<br><br>"
        index = index + 1
    write_exec_result_to_file(tp_str)


if __name__ == '__main__':
    get_weather_info()
    write_message_header()
    send_email_with_smtp()
