#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
import os
import requests
import json


def do_v2ray_check_in():
    """
    v2ray 服务器签到获取流量
    :return:
    """
    print("执行V2ray账号签到获取流量....")
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
    print(check_in_json_data)
    if check_in_json_data['msg'] == "您似乎已经签到过了...":
        print(f"已签到{check_in_json_data}")
        return 1
    elif check_in_json_data['msg'].startswith("获得了"):
        print(f"签到成功!!!\r\n{check_in_json_data}")
    else:
        print(f"签到失败!!!\r\n{check_in_json_data}")


def netease_cloud_pc_sign_in():
    print("执行网易云音乐PC端签到....")
    str_cookies = os.environ['NETEASE_CLOUD_MUSIC_PC_SIGN_COOKIES']
    str_cookie_array = str_cookies[7:].split(';')
    index = 0
    dict_netease_cloud_music_cookie = {}
    while index < len(str_cookie_array):
        str_cookie = str_cookie_array[index].split("=")
        # print(f"key={str_cookie[0].strip()} value={str_cookie[1].strip()}")
        dict_netease_cloud_music_cookie[str_cookie[0].strip()] = str_cookie[1].strip()
        index = index + 1
    post_params = os.environ['NETEASE_CLOUD_MUSIC_PC_SIGN_PARAMS']
    # print(f"cookies:{dict_netease_cloud_music_cookie}")
    # print("=============================================")
    # print(post_params)
    url = "http://interface.music.163.com/eapi/point/dailyTask"
    headers = {
                  "Accept": "*/*",
                  "Content-Type": "application/x-www-form-urlencoded",
                  "Origin": "orpheus://orpheus",
                  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome / 35.0.1916.157 Safari / 537.36",
                  "Accept-Encoding": "gzip,deflate",
                  "Accept - Language": "en - us, en;q = 0.8"
    }
    r = requests.post(url, headers=headers, cookies=dict_netease_cloud_music_cookie,data=post_params)
    print(r.text)


if __name__ == "__main__":
    do_v2ray_check_in()
    netease_cloud_pc_sign_in()
