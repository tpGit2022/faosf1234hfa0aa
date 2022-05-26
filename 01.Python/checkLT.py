#! /usr/bin/python3
# _*_ coding:UTF-8 _*_
import sys
import requests
import re
import json


const_prize_first = 99999999
const_prize_second = 999999


def check_lottery_code(input_code, release_code, lottery_type):
    """
    check prize level for kind of lottery
    :param input_code:
    :param release_code:
    :param lottery_type:  {"ssq": 1, "dlt": 281, "fc3d": 2, "pl3": 283, "pl5": 284, "qxc": 287}
    :return:
    """
    if input_code is None or release_code is None:
        return [0, -9999]
    # input_code.strip()
    # release_code.strip()
    regex = re.compile("\\s")
    input_code = regex.sub('', input_code)
    release_code = regex.sub('', release_code)
    # print(f"input_code={input_code}  release_code={release_code}")
    if lottery_type == 'pl3' or lottery_type == 'fc3d':
        if input_code == release_code:
            return [1, 1040]
        else:
            return [0, 0]
    if lottery_type == 'pl5':
        if input_code == release_code:
            return [1, 100000]
        else:
            return [0, 0]
    regex = re.compile("\\s")
    input_code = regex.sub('', input_code)
    release_code = regex.sub('', release_code)
    if lottery_type == 'ssq':
        if input_code == release_code:
            return [1, const_prize_first]
        end = input_code.index("+")
        index = 0
        front_hit = 0
        tail_hit = 0
        while index + 1 < end:
            if input_code[index] == release_code[index] and input_code[index + 1] == release_code[index + 1]:
                front_hit = front_hit + 1
            index += 2
        if input_code[end + 1] == release_code[end + 1] and input_code[end + 2] == release_code[end + 2]:
            tail_hit = 1
        if front_hit == 6 and tail_hit == 1:
            return [1, const_prize_first]
        elif front_hit == 6 and tail_hit == 0:
            return [2, const_prize_second]
        elif front_hit == 5 and tail_hit == 1:
            return [3, 3000]
        elif front_hit == 5 or (front_hit == 4 and tail_hit == 1):
            return [4, 200]
        elif front_hit == 4 or (front_hit == 3 and tail_hit == 1):
            return [5, 10]
        elif tail_hit == 1:
            return [6, 5]
        else:
            return [0, 0]

    if lottery_type == 'dlt':
        if input_code == release_code:
            return [1, const_prize_first]
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
            return [2, const_prize_second]
        elif front_hit == 5:
            return [3, 10000]
        elif front_hit == 4 and tail_hit == 2:
            return [4, 3000]
        elif front_hit == 4 and tail_hit == 1:
            return [5, 300]
        elif front_hit == 3 and tail_hit == 2:
            return [6, 200]
        elif front_hit == 4:
            return [7, 100]
        elif (front_hit == 3 and tail_hit == 1) or (front_hit == 2 and tail_hit == 2):
            return [8, 15]
        elif (front_hit == 3) or (front_hit == 2 and tail_hit == 1) or (front_hit == 1 and tail_hit == 2) or (
                tail_hit == 2):
            return [9, 5]
        else:
            return [0, 0]

    if lottery_type == 'qxc':
        if input_code == release_code:
            return [1, const_prize_first]
        end = input_code.index("+")
        index = 0
        front_hit = 0
        tail_hit = 0
        while index < end:
            if input_code[index] == release_code[index]:
                front_hit = front_hit + 1
            index = index + 1
        if input_code[end + 1] == release_code[end + 1] and input_code[end + 2] == release_code[end + 2]:
            tail_hit = 1
        if front_hit == 6 and tail_hit == 1:
            return [1, const_prize_first]
        elif front_hit == 6:
            return [2, const_prize_second]
        elif front_hit == 5 and tail_hit == 1:
            return [3, 3000]
        elif front_hit == 5 or (front_hit == 4 and tail_hit == 1):
            return [4, 500]
        elif front_hit == 4 or (front_hit == 3 and tail_hit == 1):
            return [5, 30]
        elif front_hit == 3 or tail_hit == 1:
            return [6, 5]
        else:
            return [0, 0]


def get_release_lt_code_to_check(input_code, lottery_type, start_term_nums=None, period_nums=None):
    """
    the input_code maybe dlt pls plw qxc ssq fc3d and maybe multiple term
    1.  check input_code char is correct
    2.  check input_code which type is
    3.  check prize level
    :param lottery_type: 类型
    :param period_nums: 多少期
    :param start_term_nums: 开始期号
    :param input_code:
    :return:
    """
    print(f'参数:input_code={input_code} lottery_type={lottery_type} start_term_nums={start_term_nums}  period_nums={period_nums}')
    regex = re.compile(r"[^0-9+\s,]")
    if regex.search(input_code) is not None:
        print("输入不合法,输入参数只能为数字,空格,英文加号，英文逗号")
        return
    end_term_nums = None
    if start_term_nums is not None and period_nums is not None:
        end_term_nums = int(start_term_nums) + int(period_nums) - 1
    lt_id_dict = {"ssq": 1, "dlt": 281, "fc3d": 2, "pl3": 283, "pl5": 284, "qxc": 287}
    # lt_id_list = [1, 2, 281, 283, 284, 287]
    # lotteryType = "dlt"
    issue_count = 100
    page_size = 100
    lottery_id = lt_id_dict[lottery_type]
    proxies = {"http":"http://192.168.1.117:7878/", "https:":"https://192.168.1.117:7878/"}
    url = f"https://jc.zhcw.com/port/client_json.php?transactionType=10001001&lotteryId={lottery_id}&issueCount={issue_count}&startIssue=&endIssue=&startDate=&endDate=&type=0&pageNum=1&pageSize={page_size}"
    # print(f"url={url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/98.0.4758.102 Safari/537.36",
        "DNT": "1",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Dest": "script",
        "Referer": "https://www.zhcw.com/"
    }
    r = requests.get(url, headers=headers, proxies=proxies)
    # print(r.text)
    json_data = json.loads(r.text)
    data_size = len(json_data['data'])
    index = 0
    while index < data_size:
        # print(f'issue:{json_data["data"][index]["issue"]} openTime:{json_data["data"][index]["openTime"]} ' \
        # f'frontWinningNum:{json_data["data"][index]["frontWinningNum"]} backWinningNum:{json_data["data"][index][
        # "backWinningNum"]}')
        if lottery_type == 'dlt' or lottery_type == 'ssq' or lottery_type == 'qxc':
            release_code = f'{json_data["data"][index]["frontWinningNum"]} + {json_data["data"][index]["backWinningNum"]}'
        else:
            release_code = f'{json_data["data"][index]["frontWinningNum"]}'
        if end_term_nums is None:
            ret_list = check_lottery_code(input_code, release_code, lottery_type)
            if ret_list[0] != 0:
                print(f'中奖了!!!\r\nissue:{json_data["data"][index]["issue"]}\topenTime:{json_data["data"][index]["openTime"]}-->{ret_list}')
        else:
            if end_term_nums < int(f'{json_data["data"][index]["issue"]}'):
                break
            else:
                ret_list = check_lottery_code(input_code, release_code, lottery_type)
                if ret_list[0] != 0:
                    print(f'中奖了!!!\r\nissue:{json_data["data"][index]["issue"]}\topenTime:{json_data["data"][index]["openTime"]}-->{ret_list}')
        index = index + 1


if __name__ == '__main__':
    print(f"说用说明 \"号码\" [ssq,dlt,fc3d,pl3,pl5,qxc] [开始期号] [期数]")
    print(f"示例:python xxx.py \"04 13 34 19 29 + 01 02\" dlt 21023 12")
    args_size = len(sys.argv)
    if args_size < 3:
        print("参数有误!!!")
    start_nums = None
    input_period_nums = None
    if args_size > 3:
        start_nums = sys.argv[3]
    if args_size > 4:
        input_period_nums = sys.argv[4]
    get_release_lt_code_to_check(sys.argv[1], sys.argv[2], start_nums, input_period_nums)
