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
from bs4 import BeautifulSoup

import requests

# avoid ssl error
# requests.packages.urllib3.util.ssl_1.DEFAU1LT_CIPHERS = 'ALL:@SECLEVEL=1'
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMPLEMENTOFDEFAULT"

usr_input_code = ""
list_prize_level = []
report_file_name = 'exec_result.html'
end_period_num = 99999
proxies = {
    'http': 'http://127.0.0.1:10809',
    'https': 'http://127.0.0.1:10809'
}

using_proxy = False


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


def get_lottery_info_from_office(end_period_num):
    lt_list = get_last_release_num()
    # print(f'lt_list:{lt_list}')
    current_date = lt_list[0][0]
    current_period_num = lt_list[0][1]
    origin_code = lt_list[0][2]

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
    success_msg = f"the cur period num:{current_period_num} date:{current_date}<br>the end period num:{end_period_num}" \
                  f"<br>usr_input_code:{usr_input_code}<br>office_rea_code:{origin_code}<br><br><br>"
    # write_exec_result_to_file(success_msg)
    # print office release code
    lt_index = 0
    while lt_index < len(lt_list) and lt_index < 4:
        office_release_origin_code = lt_list[lt_index][2]
        # print(f"office release code:{office_release_origin_code}")
        success_msg = success_msg + f"office release code:{office_release_origin_code}<br>"
        print(
            f"office release code:发售日期:{lt_list[lt_index][0]} 期号:{lt_list[lt_index][1]} 发布:{lt_list[lt_index][2]}")
        lt_index = lt_index + 1
    write_exec_result_to_file(success_msg)
    print(f"{current_period_num} {end_period_num}")
    if (end_period_num - 2) <= int(current_period_num):
        # avoid too much email send to user if beyond date to much
        return True
    else:
        return False


def get_last_release_num() -> list:
    """
    获取最新的公布的信息
    尝试多个渠道只返回一组有效的list，一条list包含多组元组数据(日期，期号，号码)
    :return:
    """
    gdtc_lst = None
    gstc_list = None
    try:
        gdtc_lst = get_last_info_from_gdtc()
    except Exception as e:
        print('gdtc获取数据出错')
        print(e.args)
    print(f'gdtc:{gdtc_lst}')
    try:
        gstc_list = get_last_info_from_gstc()
    except Exception as e:
        print('gstc获取数据出错')
        print(e.args)
    print(f'gstc:{gstc_list}')
    if (gdtc_lst is None or len(gdtc_lst) <= 0) and (gstc_list is None or len(gstc_list) <= 0):
        print('未正常获取到数据')
        sys.exit(-1)
    if gdtc_lst is None or len(gdtc_lst) <= 0:
        return gstc_list
    if gstc_list is None or len(gstc_list) <= 0:
        return gdtc_lst
    return gstc_list
    pass


def get_last_info_from_gdtc() -> list:
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
    if using_proxy:
        r = requests.get(url, headers=headers, proxies=proxies)
    else:
        r = requests.get(url, headers=headers)
    # print(r.text)
    lt_list = json.loads(r.text)
    origin_code = lt_list[0]["kjhm"]
    current_period_num = int(lt_list[0]['drawid'])
    current_date = lt_list[0]['saleDate']

    # print(f"office_release_code={origin_code}")
    origin_code = origin_code.replace(" ", "@")
    origin_code = origin_code.replace("+", " ")
    origin_code = origin_code.replace("@", "+")
    lt_list = [(current_date, current_period_num, origin_code)]
    return lt_list
    pass


def get_last_info_from_gstc() -> list:
    url = 'https://www.gstc.org.cn/super_lotto/historical_record'
    gstc_list = None
    http_header = {
        "Host": "www.gstc.org.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }
    if using_proxy:
        response = requests.get(url, headers=http_header, proxies=proxies)
    else:
        response = requests.get(url, headers=http_header)
    # print(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    element = soup.select('.content-box > ul > li')
    for i in range(0, len(element) - 3):
        element_content = element[i].text
        release_date = element_content[:10]
        release_code = element_content[11:16]
        release_num = element_content[17:]
        release_num = release_num[:2] + ' ' + release_num[2:4] + ' ' \
                      + release_num[4:6] + ' ' + release_num[6:8] + ' ' \
                      + release_num[8:10] + '+' + release_num[10:12] + ' ' + release_num[12:14]
        # print(f'{release_date}\t{release_code}\t{release_num}')
        gstc_list = [(release_date, int(release_code), release_num)]
        break
        pass
    return gstc_list


def write_exec_result_to_file(log_str):
    with open(report_file_name, mode="a+", encoding="UTF-8") as file:
        input_str = f"<br>{log_str}"
        file.write(input_str)


def write_message_header():
    m_time_stamp = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    tp_str = f"<br><br>===================================" \
             f"<br>the python exec at {m_time_stamp}" \
             f"<br>===================================<br>"
    write_exec_result_to_file(tp_str)


def send_email_with_smtp(is_out_dated):
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
        email_subject = f"临近截至日期了!!!"
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
        # is_outdated = check_outdated(period_nums=int(term_period), start_time=start_time)
    end_period_num = int(start_period_nums) + int(term_period) - 1
    print(f"实际截至有效期号:{end_period_num}")
    is_outdated = get_lottery_info_from_office(end_period_num)
    # need_send_email = True
    send_email_with_smtp(is_out_dated=is_outdated)
    # clean work, delete exec_result.html
    if os.path.exists("exec_result.html"):
        os.remove("exec_result.html")


if __name__ == '__main__':
    fun_exec()
