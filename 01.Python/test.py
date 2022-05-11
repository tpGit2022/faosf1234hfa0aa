#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
import sys

import requests


def checkNum(hit, input):
    r = requests.get("https://mirrors.tuna.tsinghua.edu.cn/AdoptOpenJDK/8/jdk/x64/windows/")
    if r.status_code == 200:
        print(r.encoding)
        file = open("test.html", mode="w", encoding="ISO-8859-1")
        file.write(r.text)


if __name__ == "__main__":
    checkNum(1, 1)
