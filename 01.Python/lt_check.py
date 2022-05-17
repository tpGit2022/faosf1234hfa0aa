#! /usr/bin/python3
# _*_ coding:UTF-8 _*_

import re
import sys


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def lottery_code_check(input_code, release_code):
    """
    check code
    :param input_code: the code you buy
    :param release_code: the code publish by office
    :return: the prize
    """
    input_code = input_code.lstrip()
    input_code = input_code.rstrip()
    release_code = release_code.lstrip()
    release_code = release_code.rstrip()

    if input_code.find("+") < 0:
        return [0, -998]
    if release_code.find("+") < 0:
        return [0, -999]

    regex = re.compile("\\s")
    input_code = regex.sub('', input_code)
    release_code = regex.sub('', release_code)
    if input_code == release_code:
        return [1, 9999]
    end = input_code.index("+")
    index = 0
    front_hit = 0
    tail_hit = 0
    # print(f"input len({len(input_code)}) release len({len(release_code)})")
    while index + 1 < end:
        if input_code[index] == release_code[index] and input_code[index + 1] == release_code[index + 1]:
            front_hit = front_hit + 1
        index += 2
    index = end + 1
    while index + 1 < len(input_code):
        if input_code[index] == release_code[index] and input_code[index + 1] == release_code[index + 1]:
            tail_hit = tail_hit + 1
        index += 2
    if front_hit == 5 and tail_hit == 1:
        return [2, 999]
    if front_hit == 5:
        return [3, 10000]
    if front_hit == 4 and tail_hit == 2:
        return [4, 3000]
    if front_hit == 4 and tail_hit == 1:
        return [5, 300]
    if front_hit == 3 and tail_hit == 2:
        return [6, 200]
    if front_hit == 4:
        return [7, 100]
    if (front_hit == 3 and tail_hit == 1) or (front_hit == 2 and tail_hit == 2):
        return [8, 15]
    if (front_hit == 3) or (front_hit == 2 and tail_hit == 1) or (front_hit == 1 and tail_hit == 2) or (tail_hit == 2):
        return [9, 5]
    return [0, 0]


if __name__ == '__main__':
    print(sys.argv[0])
    level = lottery_code_check("10 15 19 28 32 + 04 09", "10 15 19 28 32 + 04 09")
    if level == 1:
        print("big price")
    else:
        print(level)
    if len(sys.argv) >= 2:
        print(f"参数为:{sys.argv[1]}")
        out_file_name = "123456.txt"
        file = open(out_file_name, mode="w", encoding="UTF-8")
        input = f"第二个参数是:{sys.argv[1]} \n<br> 第三个参数:{sys.argv[2]} \n<br> 第四个参数:{sys.argv[3]}"
        file.write(input)


