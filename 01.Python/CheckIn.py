#! /usr/bin/python3
# _*_ coding:UTF-8 _*_
import os
import requests
import json


def do_v2ray_check_in():
    """
    v2ray 服务器签到获取流量
    :return:
    """
    login_url = "https://ssru6.pw/auth/login"
    headers = {
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        "DNT": "1",
        "sec-ch-ua-mobile": '?0',
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        "Content-Type": 'application/x-www-form-urlencoded; charset=UTF-8',
        "Accept": 'application/json, text/javascript, */*; q=0.01',
        "X-Requested-With": 'XMLHttpRequest',
        "sec-ch-ua-platform": '"Windows"',
        "Origin": 'https://ssru6.pw',
        "Sec-Fetch-Site": 'same-origin',
        "Sec-Fetch-Mode": 'cors',
        "Sec-Fetch-Dest": 'empty',
        "Referer": 'https: // ssru6.pw / auth / login'
    }
    v2ray_server_user_name = os.environ['V2RAY_SERVER_USER_NAME']
    v2ray_server_user_pwd = os.environ['V2RAY_SERVER_USER_PWD']
    data_dict = {'email': v2ray_server_user_name, 'passwd': v2ray_server_user_pwd, 'code': ''}
    # print(data_dict)
    r = requests.post(login_url, data=data_dict, headers=headers)
    print(r.text)

    json_data = json.loads(r.text)
    # 判断是否登录成功
    if json_data.get('msg', '') != "登录成功":
        print("登录失败")
        return -1
    else:
        print("登录成功!!!!!!,开始执行签到工作")
    check_in_url = "https://ssru6.pw/user/checkin"
    headers = {
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        "DNT": "1",
        "sec-ch-ua-mobile": '?0',
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        "Accept": 'application/json, text/javascript, */*; q=0.01',
        "X-Requested-With": 'XMLHttpRequest',
        "sec-ch-ua-platform": '"Windows"',
        "Origin": 'https://ssru6.pw',
        "Sec-Fetch-Site": 'same-origin',
        "Sec-Fetch-Mode": 'cors',
        "Sec-Fetch-Dest": 'empty',
        "Referer": 'https: // ssru6.pw / auth / login'
    }
    check_r = requests.post(check_in_url, headers=headers, cookies=r.cookies)
    check_in_json_data = json.loads(check_r.text)
    if check_in_json_data['msg'] == "您似乎已经签到过了...":
        print(f"已签到{check_in_json_data}")
        return 1
    elif check_in_json_data['msg'].startwith("获得了"):
        print(f"签到成功!!!\r\n{check_in_json_data}")
    else:
        print(f"签到失败!!!\r\n{check_in_json_data}")


if __name__ == '__main__':
    do_v2ray_check_in()
