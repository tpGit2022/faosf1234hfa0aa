#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
import os


def checkNum():
    print(os.environ['ENV_TEST'])
    print(os.environ['EMAIL_TEST_TEST'])
    print(os.environ['pythonLocation'])
    print()
    print(os.environ)


if __name__ == "__main__":
    checkNum()
