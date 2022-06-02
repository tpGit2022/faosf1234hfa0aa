#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
import os


def checkNum():
    print(os.environ['ENV_TEST'])


if __name__ == "__main__":
    checkNum(1, 1)
