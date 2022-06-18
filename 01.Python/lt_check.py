#! /usr/bin/python3
# _*_ coding:UTF-8 _*_

import json
import os
import re
import smtplib
import sys
import time
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr
from datetime import datetime, timedelta

import requests

# avoid ssl error
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'

usr_input_code = ""
list_prize_level = []
report_file_name = 'exec_result.html'


def lottery_code_check(input_code, release_code):
    """
    check code
    :param input_code: the code you buy
    :param release_code: the code publish by office
    :return: the prize
    """
    # print(f"input_code={input_code} release_code={release_code}")
    input_code = input_code.strip()
    release_code = release_code.strip()

    if input_code.find("+") < 0:
        return [0, -998]
    if release_code.find("+") < 0:
        return [0, -999]

    regex = re.compile("\\s")
    input_code = regex.sub('', input_code)
    release_code = regex.sub('', release_code)
    if input_code == release_code:
        return [1, 9999]
    end = input_code.index("+")
    index = 0
    front_hit = 0
    tail_hit = 0
    # print(f"input len({len(input_code)}) release len({len(release_code)})")
    while index + 1 < end:
        if input_code[index] == release_code[index] and input_code[index + 1] == release_code[index + 1]:
            front_hit = front_hit + 1
        index += 2
    index = end + 1
    while index + 1 < len(input_code):
        if input_code[index] == release_code[index] and input_code[index + 1] == release_code[index + 1]:
            tail_hit = tail_hit + 1
        index += 2
    if front_hit == 5 and tail_hit == 1:
        return [2, 999]
    if front_hit == 5:
        return [3, 10000]
    if front_hit == 4 and tail_hit == 2:
        return [4, 3000]
    if front_hit == 4 and tail_hit == 1:
        return [5, 300]
    if front_hit == 3 and tail_hit == 2:
        return [6, 200]
    if front_hit == 4:
        return [7, 100]
    if (front_hit == 3 and tail_hit == 1) or (front_hit == 2 and tail_hit == 2):
        return [8, 15]
    if (front_hit == 3) or (front_hit == 2 and tail_hit == 1) or (front_hit == 1 and tail_hit == 2) or (tail_hit == 2):
        return [9, 5]
    return [0, 0]


def get_lottery_info_from_office():
    url = "https://www.gdlottery.cn/gdata/idx/tcnotice"
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
    # print(r.text)
    lt_list = json.loads(r.text)
    origin_code = lt_list[0]["kjhm"]
    # print(f"office_release_code={origin_code}")
    origin_code = origin_code.replace(" ", "@")
    origin_code = origin_code.replace("+", " ")
    origin_code = origin_code.replace("@", "+")
    ret_list = lottery_code_check(usr_input_code, origin_code)
    global list_prize_level
    list_prize_level = ret_list
    if ret_list[0] != 0:
        regex = re.compile("\\s")
        tp_input_code = regex.sub('', usr_input_code)
        tp_release_code = regex.sub('', origin_code)
        tp_str = f"<br>Congratulate you are so lucky {ret_list}<br><br>input_code-->release_code:" \
                 f"<br><br>{tp_input_code}<br>{tp_release_code} "
        write_exec_result_to_file(tp_str)
    else:
        tp_str = f"<br>nothing hit...<br>"
        write_exec_result_to_file(tp_str)
    success_msg = f"<br>python exec as expect"
    write_exec_result_to_file(success_msg)
    # print office release code
    lt_index = 0
    while lt_index < len(lt_list):
        office_release_origin_code = lt_list[lt_index]["kjhm"]
        print(f"office release code:{office_release_origin_code}")
        lt_index = lt_index + 1


def write_exec_result_to_file(log_str):
    with open(report_file_name, mode="a+", encoding="UTF-8") as file:
        input_str = f"<br>{log_str}"
        file.write(input_str)


def write_message_header():
    m_time_stamp = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    tp_str = f"<br><br>==============================================================================" \
             f"<br>the python exec at {m_time_stamp}" \
             f"<br>==============================================================================<br>"
    write_exec_result_to_file(tp_str)


def write_message_tailer():
    r = requests.get("https://ip.gs/json")
    json_str = json.loads(r.text)
    # print(json_str)
    print(f"IP:{json_str['ip']} City:{json_str.get('city', None)} TimeZone:{json_str['time_zone']}")
    tp_str = f"<br><br><br>==============================================================================" \
             f"<br>IP:{json_str['ip']}<br>Country:{json_str['country']}<br>" \
             f"Region:{json_str.get('region_name', None)}" \
             f"<br>City:{json_str.get('city', None)}<br>Latitude:{json_str.get('latitude', None)}\t" \
             f"longitude:{json_str.get('longitude', None)}" \
             f"<br>TimeZone:{json_str['time_zone']}<br>asnOrg:{json_str.get('asn_org', None)}" \
             f"<br>==============================================================================<br>"
    write_exec_result_to_file(tp_str)


def send_email_with_smtp(is_out_dated, end_period_nums):
    print(f"send_email_with_smtp is_out_dated={is_out_dated} list_prize_level={list_prize_level}")
    if not is_out_dated and list_prize_level[0] == 0:
        print("GitHub Action Python Script, Do not trigger Send Email Action")
        return

    # print(os.environ)
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
    msg['From'] = formataddr((Header("小秘书", "UTF-8").encode(), "this_addr_is_random_write@qq.com"))
    msg['To'] = f"{email_config_server_recv_user_name}"
    email_subject = ""
    if list_prize_level[0] == 1 or list_prize_level[0] == 2:
        email_subject = f"您中了超巨奖!!!!  {list_prize_level[0]}等奖"
    elif list_prize_level[0] != 0:
        email_subject = f"您中了{list_prize_level[1]}"
    if is_out_dated:
        email_subject = f"最后期号{end_period_nums},临近截至日期了!!!"
    msg['Subject'] = Header(email_subject, 'UTF-8').encode()

    smtp_obj = smtplib.SMTP_SSL(email_config_server_domain, int(email_config_server_port))
    # smtp_obj.set_debuglevel(1)
    smtp_obj.login(user=email_config_server_user_name, password=email_config_server_user_pwd)
    smtp_obj.sendmail(email_config_server_user_name, email_config_server_recv_user_name, msg.as_string())
    smtp_obj.quit()


def check_outdated(period_nums, start_time):
    """

    :param period_nums: the period nums
    :param start_time: start_time like 2020_02_10
    :return: True is outdated False is valid
    """
    if period_nums <= 2:
        return True
    f_start_time = datetime.strptime(start_time, '%Y_%m_%d')
    gap_days = ((period_nums - 1) / 3) * 7 - 3
    ddl_time = f_start_time + timedelta(days=gap_days)
    out_date_log = f"ddl_time={ddl_time} now_time={f_start_time.now()}"
    print(out_date_log)
    write_exec_result_to_file(out_date_log)
    if f_start_time.now() >= ddl_time:
        return True
    return False


def fun_exec():
    write_message_header()
    global usr_input_code
    usr_input_code = os.environ['LT_INPUT_CODE']
    is_outdated = False
    if len(sys.argv) >= 3:
        # time_stamp = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
        term_period = sys.argv[1]
        start_time = sys.argv[2]
        start_period_nums = sys.argv[3]
        # print(f"time_stamp={time_stamp} start_time={start_time} term_period={term_period}")
        is_outdated = check_outdated(period_nums=int(term_period), start_time=start_time)
    get_lottery_info_from_office()
    write_message_tailer()
    # need_send_email = True
    send_email_with_smtp(is_out_dated=is_outdated, end_period_nums = start_period_nums + term_period - 1)
    # clean work, delete exec_result.html
    if os.path.exists("exec_result.html"):
        os.remove("exec_result.html")


if __name__ == '__main__':
    fun_exec()
