#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
import os
import requests
import json
import urllib3
urllib3.disable_warnings()

using_proxy = False

proxy_fiddler = {
    "http": "http://127.0.0.1:7878",
    "https": "http://127.0.0.1:7878"
}

proxy_v2ray = {
    "http": "http://127.0.0.1:10809",
    "https": "http://127.0.0.1:10809"
}

http_proxy = proxy_fiddler


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
    check_ok_response = [0x43, 0xAE, 0xB2, 0x16, 0x3B, 0x20, 0xEC, 0xB9, 0x8A, 0x32, 0x86,
                         0x7C, 0x53, 0xCD, 0xA3, 0x18, 0x48, 0x4D, 0x32, 0xBB, 0x9E, 0x8B,
                         0xDA, 0xCC, 0x66, 0x57, 0x31, 0x29, 0x5B, 0x97, 0xA6, 0x8B]
    has_checked_response = [0xC8, 0x76, 0x3D, 0xA4, 0xEF, 0x8E, 0x9A, 0x8D, 0x40, 0x96, 0x2E,
                            0x24, 0x8C, 0x8C, 0x34, 0x80, 0xFD, 0x26, 0xCD, 0x1C, 0x30, 0xB2, 0x42,
                            0x32, 0x0C, 0x3B, 0x24, 0xA1, 0x83, 0xB9, 0x73, 0x3B, 0x6A, 0xA3, 0xB1, 0x02,
                            0xFB, 0xE7, 0x29, 0x6A, 0xB0, 0xDB, 0x9E, 0xA5, 0xC4, 0x6A, 0xD1, 0x2B]
    response_list = list(r.content)
    if check_ok_response == response_list:
        print('网易云签到成功')
    elif has_checked_response == response_list:
        print('网易云已经签过到了')
    else:
        print('签到失败返回结果:')
        print(response_list)


def netease_note_checkin():
    """
    有道云笔记签到
    :return:
    """
    post_url = 'https://note.youdao.com/yws/mapi/user?method=checkin'
    request_header = {
        "User-Agent": "ynote-android",
        "Cookie": f"{os.environ['NETEASE_CLOUD_NOTE_COOKIES']}",
        "Accept-Encoding": "gzip",
        "Accept-Charset": "GBK,utf-8;q=0.7,*;q=0.3",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "483",
        "Host": "note.youdao.com",
        "Connection": "Keep-Alive"
    }
    post_data = f"{os.environ['NETEASE_CLOUD_NOTE_POST_DATA']}"
    if using_proxy:
        r = requests.post(url=post_url, headers=request_header, data= post_data, proxies= http_proxy, verify=False)
    else:
        r = requests.post(url=post_url, headers=request_header, data= post_data)
    print(r.text)
    pass


if __name__ == "__main__":
    # do_v2ray_check_in()
    # print(os.path.abspath(__file__))
    netease_cloud_pc_sign_in()
    netease_note_checkin()
