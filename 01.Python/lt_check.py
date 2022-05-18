#! /usr/bin/python3
# _*_ coding:UTF-8 _*_

import re
import sys
import json
import requests
import time

usr_input_code = ""
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
    url = "https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry?gameNo=85&provinceId=0&pageSize=30&isVerify=1&pageNo=1&termLimits=30"
    try:
        r = requests.get(url)
        dict = json.loads(r.text)
        data_list = dict["value"]["list"]
        # data_len  = len(data_list)
        # for index in range(data_len):
        #     print(f'{data_list[index]["lotteryDrawTime"]}:{data_list[index]["lotteryDrawResult"]}')
        for data in data_list:
            # print(f'{data["lotteryDrawTime"]}:{data["lotteryDrawResult"]}')
            tp_list = list(data["lotteryDrawResult"])
            tp_list.insert(-6, " ")
            tp_list.insert(-6, "+")
            # print(tp_list)
            office_code = ''.join(tp_list)
            # global usr_input_code
            # usr_input_code = "11 14 22 23 27 + 08 10"
            result_list = lottery_code_check(usr_input_code, office_code)
            if result_list[0] != 0:
                rs = f'{data["lotteryDrawTime"]} --> {data["lotteryDrawResult"]} --> result:{result_list}'
                print(rs)
                write_exec_result_to_file(rs)

    except Exception as ex:
        print(f"Error {ex}")

    else:
        print("ok")

def write_exec_result_to_file(str):
    out_file_name = "exec_result.html"
    file = open(out_file_name, mode="a+", encoding="UTF-8")
    input = f"<br>{str}"
    file.write(input)

def write_time_info():
    time_stamp = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    tp_str = f"the python exec at {time_stamp}"
    write_exec_result_to_file(tp_str)


if __name__ == '__main__':
    write_time_info()
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


