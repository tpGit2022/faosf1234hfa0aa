#! /usr/bin/python3
# _*_ coding:UTF-8 _*_
import os

import requests
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMPLEMENTOFDEFAULT"

http_get_headers = {
    "Host":"weread.qnmlgb.tech",
    "Connection":"keep-alive",
    "sec-ch-ua":'" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
    "sec-ch-ua-mobile":"?0",
    "sec-ch-ua-platform":"Windows",
    "DNT":"1",
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site":"same-origin",
    "Sec-Fetch-Mode":"navigate",
    "Sec-Fetch-User":"?1",
    "Sec-Fetch-Dest":"document",
    "Referer":"https://weread.qnmlgb.tech/onestep",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cookie":"weread_searchtext=394644486;"
}


def weixin_group_task_commit():
    task_id = os.environ['WEIXIN_READ_TASK_ID']
    task_url = f'https://weread.qnmlgb.tech/onestep_submit/{task_id}?action=link'
    r = requests.get(task_url, headers=http_get_headers)
    print(r.text)
    pass


if __name__ == '__main__':
    weixin_group_task_commit()