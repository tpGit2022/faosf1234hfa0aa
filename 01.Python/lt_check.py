#! /usr/bin/python3
# _*_ coding:UTF-8 _*_

import json
import os
import re
import sys
import time
import requests
import smtplib
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

# avoid ssl error
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'

usr_input_code = ""
need_send_email = False
def lottery_code_check(input_code, release_code):
    """
    check code
    :param input_code: the code you buy
    :param release_code: the code publish by office
    :return: the prize
    """
    input_code = input_code.lstrip()
    input_code = input_code.rstrip()
    release_code = release_code.lstrip()
    release_code = release_code.rstrip()

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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        "DNT": "1",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.gdlottery.cn/?v=1652849733245"
    }
    r = requests.get(url, headers= headers)
    print(r.text)
    # write_exec_result_to_file(r.text)
    lt_list = json.loads(r.text)
    origin_code = lt_list[0]["kjhm"]
    print(f"origin_code={origin_code}")
    origin_code = origin_code.replace(" ", "@")
    origin_code = origin_code.replace("+", " ")
    origin_code = origin_code.replace("@", "+")
    ret_list = lottery_code_check(usr_input_code, origin_code)
    if ret_list[0] !=0:
        print(ret_list)
        tp_str = f"<br>Congratulate you are so lucky {ret_list}<br>"
        write_exec_result_to_file(tp_str)
    else:
        tp_str = f"<br>nothing hit...<br>"
        write_exec_result_to_file(tp_str)

    # data_list = dict["value"]["list"]
    #     # data_len  = len(data_list)
    #     # for index in range(data_len):
    #     #     print(f'{data_list[index]["lotteryDrawTime"]}:{data_list[index]["lotteryDrawResult"]}')
    # for data in data_list:
    #         # print(f'{data["lotteryDrawTime"]}:{data["lotteryDrawResult"]}')
    #     tp_list = list(data["lotteryDrawResult"])
    #     tp_list.insert(-6, " ")
    #     tp_list.insert(-6, "+")
    #         # print(tp_list)
    #     office_code = ''.join(tp_list)
    #         # global usr_input_code
    #         # usr_input_code = "11 14 22 23 27 + 08 10"
    #     result_list = lottery_code_check(usr_input_code, office_code)
    #     if result_list[0] != 0:
    #         rs = f'{data["lotteryDrawTime"]} --> {data["lotteryDrawResult"]} --> result:{result_list}'
    #         print(rs)
    #         write_exec_result_to_file(rs)

    # except Exception as ex:
    # error_msg = f"<br> python script exec exception see the info:<br>${ex}"
    # write_exec_result_to_file(error_msg)
    # else:
    success_msg = f"<br>python exec as expect"
    write_exec_result_to_file(success_msg)

def write_exec_result_to_file(str):
    out_file_name = "exec_result.html"
    file = open(out_file_name, mode="a+", encoding="UTF-8")
    input = f"<br>{str}"
    file.write(input)

def write_message_header():
    time_stamp = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    tp_str = f"the python exec at {time_stamp}"
    r = requests.get("https://ip.gs/json")
    json_str = json.loads(r.text)
    print(json_str)
    tp_str = tp_str + f"<br>IP:{json_str['ip']}<br>Country:{json_str['country']}<br>Region:{json_str['region_name']}" \
                      f"<br>City:{json_str['city']}<br>Latitude:{json_str['latitude']}\tlongitude:{json_str['longitude']}" \
                      f"<br>TimeZone:{json_str['time_zone']}"
    write_exec_result_to_file(tp_str)

def send_email_with_smtp():
    if need_send_email != True:
        print("Github Action Python Script, Do not trigger Send Email Action")
        return
    # py3_env = os.environ['PYTHON3HOME']
    # email_config_server_domain = os.environ['EMAIL_SMTP_DOMAIN']
    # email_config_server_port = os.environ['EMAIL_SMTP_PORT']
    # email_config_server_user_name = os.environ['EMAIL_SMTP_USER_NAME']
    # email_config_server_user_pwd = os.environ['EMAIL_SMTP_USER_PWD']
    # email_config_server_recv_user_name = os.environ['EMAIL_SMTP_REV']

    # smtp_obj.starttls()
    msg = MIMEText('hello\nfsfsfs\nsfsafasfas\nsfasfasfdas\nsfasdfas\nfsfas\r\nfasfasfs<br>fasfdasfd', 'plain', 'UTF-8')
    msg['From'] = formataddr(['smtp_python_user_name', 'tp_net_cloud@163.com'])
    msg['To'] = Header('1379126606@qq.com', 'UTF-8')
    msg['Subject'] = Header('test python email module', 'UTF-8').encode()
    smtp_obj = smtplib.SMTP_SSL("smtp.163.com", "465")

    #smtp_obj.set_debuglevel(1)
    smtp_obj.login(user="tp_net_cloud@163.com", password="CSLMENAXCRLOPQDW")
    smtp_obj.sendmail('tp_net_cloud@163.com', ['1379126606@qq.com'], msg.as_string())
    smtp_obj.quit()

if __name__ == '__main__':
    send_email_with_smtp()
    write_message_header()
    # level = lottery_code_check("10 15 19 28 32 + 04 09", "10 15 19 28 32 + 04 09")
    if len(sys.argv) >= 2:
        usr_input_code = sys.argv[1]
        # print(f"参数为:{sys.argv[1]}")
        # out_file_name = "exec_result.html"
        # file = open(out_file_name, mode="w", encoding="UTF-8")
        # input = f"第二个参数是:{sys.argv[1]} \n<br> 第三个参数:{sys.argv[2]} \n<br> 第四个参数:{sys.argv[3]}"
        # file.write(input)
        # print(f"usr_input_code:{usr_input_code}")
    get_lottery_info_from_office()


