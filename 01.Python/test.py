#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
import os
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr


def checkNum():
    print(os.environ['ENV_TEST'])
    print(os.environ['pythonLocation'])
    print()
    print(os.environ)
    send_email_with_smtp(os.environ['ENV_TEST'])


def send_email_with_smtp(subject_content):
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
    msg = MIMEText("report_string", 'plain', 'UTF-8')
    msg['From'] = formataddr((Header("小秘书", "UTF-8").encode(), "this_addr_is_random_write@qq.com"))
    msg['To'] = f"{email_config_server_recv_user_name}"
    msg['Subject'] = Header(subject_content, 'UTF-8').encode()

    smtp_obj = smtplib.SMTP_SSL(email_config_server_domain, int(email_config_server_port))
    # smtp_obj.set_debuglevel(1)
    smtp_obj.login(user=email_config_server_user_name, password=email_config_server_user_pwd)
    smtp_obj.sendmail(email_config_server_user_name, email_config_server_recv_user_name, msg.as_string())
    smtp_obj.quit()


if __name__ == "__main__":
    checkNum()
