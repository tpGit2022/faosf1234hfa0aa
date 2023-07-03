#! /usr/bin/python3
# _*_ coding:UTF-8 _*_
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr

import requests
from bs4 import BeautifulSoup
import os

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMPLEMENTOFDEFAULT"

proxies = {
    "http": "http://127.0.0.1:10809",
    "https": "http://127.0.0.1:10809"
}

using_proxy = False

email_config_smtp_server_domain = ''
email_config_smtp_server_port = ''
email_config_server_user_name = ''
email_config_server_user_pwd = ''
email_config_server_recv_user_email_addr = ''
email_config_black_hole_addr = ''


def login_remote_server():
    login_url = "https://ssru6.pw/auth/login"
    headers = {
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        "DNT": "1",
        "sec-ch-ua-mobile": '?0',
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/98.0.4758.102 Safari/537.36',
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
    if using_proxy:
        r = requests.post(login_url, data=data_dict, headers=headers, proxies=proxies)
    else:
        r = requests.post(login_url, data=data_dict, headers=headers)
    print(r.text)
    return r.cookies


def get_remote_server_proxy_list(server_cookies):
    """
    获取V2ray服务器所有节点的VMESS协议链接
    :param server_cookies:
    :return:
    """
    proxy_node_list_url = "https://ssru6.pw/user/node"
    headers = {
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        "DNT": "1",
        "sec-ch-ua-mobile": '?0',
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        "Content-Type": 'application/x-www-form-urlencoded; charset=UTF-8',
        "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        "sec-ch-ua-platform": '"Windows"',
        "referer": "https://ssru6.pw/user/node",
        "Sec-Fetch-Site": 'same-origin',
        "Sec-Fetch-Mode": 'navigate',
        "Sec-Fetch-Dest": 'document',
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "Referer": 'https: // ssru6.pw / auth / login'
    }
    if using_proxy:
        r = requests.get(url=proxy_node_list_url, headers=headers, proxies=proxies, cookies=server_cookies)
    else:
        r = requests.get(url=proxy_node_list_url, headers=headers, cookies=server_cookies)
    soup = BeautifulSoup(r.text, "html.parser")
    blocks_a = soup.find_all("a", class_="copy-text")
    index = len(blocks_a) - 1
    server_link_list = []
    while index >= 0:
        server_link = blocks_a[index].attrs['data-clipboard-text']
        # print(server_link)
        server_link_list.append(server_link)
        index = index - 1
    print(len(blocks_a))
    return server_link_list


def send_server_link_list_to_email(servers):
    report_string = '\r\n'.join(servers)
    msg = MIMEText(report_string, 'plain', 'UTF-8')
    msg['From'] = formataddr((Header("get_proxy_list", "UTF-8").encode(), "get_proxy_list@qq.com"))
    msg['To'] = f"{email_config_black_hole_addr}"
    v2ray_server_user_pwd = os.environ['V2RAY_SERVER_USER_PWD']
    # email_subject = "get_proxy_list_github_action"
    email_subject = os.environ['V2RAY_SERVER_USER_NAME']
    msg['Subject'] = Header(email_subject, 'UTF-8').encode()
    smtp_obj = smtplib.SMTP_SSL(email_config_smtp_server_domain, int(email_config_smtp_server_port))
    # if need print debug message to track bugs, open it
    # smtp_obj.set_debuglevel(1)
    smtp_obj.login(user=email_config_server_user_name, password=email_config_server_user_pwd)
    smtp_obj.sendmail(email_config_server_user_name, email_config_black_hole_addr, msg.as_string())
    smtp_obj.quit()
pass


def init_email_config():
    global email_config_smtp_server_domain
    email_config_smtp_server_domain = os.environ['EMAIL_SMTP_DOMAIN']
    global email_config_smtp_server_port
    email_config_smtp_server_port = os.environ['EMAIL_SMTP_PORT']
    global email_config_pop3_server_domain
    # email_config_pop3_server_domain = os.environ['EMAIL_POP3_DOMAIN']
    # global email_config_pop3_server_port
    # email_config_pop3_server_port = os.environ['EMAIL_POP3_PORT']
    global email_config_server_user_name
    email_config_server_user_name = os.environ['EMAIL_SMTP_USER_NAME']
    global email_config_server_user_pwd
    email_config_server_user_pwd = os.environ['EMAIL_SMTP_USER_PWD']
    global email_config_server_recv_user_email_addr
    email_config_server_recv_user_email_addr = os.environ['EMAIL_SMTP_REV']
    global email_config_black_hole_addr
    email_config_black_hole_addr = os.environ['EMAIL_BLACK_HOLE_ADDR']

    pass


if __name__ == "__main__":
    init_email_config()
    request_cookies = login_remote_server()
    server_link_list = get_remote_server_proxy_list(request_cookies)
    send_server_link_list_to_email(server_link_list)
    pass
