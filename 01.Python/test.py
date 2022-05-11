#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
import sys

import requests
import time

def checkNum(hit, input):
    r = requests.get("https://mirrors.tuna.tsinghua.edu.cn/AdoptOpenJDK/8/jdk/x64/windows/")
    if r.status_code == 200:
        # print(r.encoding)
        time_ticket = time.strftime("%Y_%m_%d", time.localtime())
        str_format = "{timestamp:s}.html"
        out_file_name = str_format.format(timestamp=time_ticket)
        print(out_file_name)
        file = open(out_file_name, mode="w", encoding="ISO-8859-1")
        file.write(r.text)


if __name__ == "__main__":
    checkNum(1, 1)
