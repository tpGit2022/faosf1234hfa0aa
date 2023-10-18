#! /usr/bin/python3
# _*_ coding:UTF-8 _*_
import base64
import hashlib
import os
import sys
from pathlib import Path
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

tp_path = Path(os.path.abspath(__file__))

"""
"""
aes_file_encrypt_key = os.environ['FILE_ENCRYPT_DECRYPT_KEY']

decide_list_dict = {
    'encrypt_data': 0,
    'decrypt_data': 1
}
initial_vector = 'aes_256_initial_vector'[0:16]
origin_media_base_dir = None
encrypt_base_dir = None
decrypt_base_dir = None

# 代表自定义文件头MD之后的开始索引
BASE_INDEX_START = 64
BLOCK_SIZE = 16
FILE_BLOCK_SIZE = 1024 * 256
FILE_MAGIC_NUMBER = 28
MD5_LENGTH = 32

isDebug = False

# # 填充函数，填充模式：PKCS5Padding(填充内容等于缺少的字节数)
# pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE).encode()
# # 返填充函数
# unpad = lambda s: s[:-ord(s[len(s) - 1:])]

class FileInfo:
    def __init__(self):
        self.file_name = ''
        self.file_head_version = ''
        self.file_md5 = ""
        self.file_size = 0
        self.file_size_bytes_count = 0
        self.file_name_bytes = ""
        self.file_name_bytes_count = 0
        self.file_head_bytes_count = 0

    def __str__(self):
        return f"文件名: {self.file_name}, 加密版本 V{self.file_head_version}, " \
               f"MD5: {self.file_md5}, 文件大小: {self.file_size}, " \
               f"文件大小字节数: {self.file_size_bytes_count}, " \
               f"文件名: {self.file_name_bytes}, 文件名字节数: {self.file_name_bytes_count}" \
               f"文件头字节数: {self.file_head_bytes_count}"


def get_ase_encrypt_key() -> bytes:
    base64_encode_key = base64.standard_b64encode(aes_file_encrypt_key.encode('UTF-8'))
    md5_key = hashlib.md5(base64_encode_key)
    return md5_key.digest()


def get_file_md5(input_file_path) -> str:
    md5 = hashlib.md5()
    with open(input_file_path, 'rb') as input_f:
        for chunk in iter(lambda: input_f.read(8192), b''):
            md5.update(chunk)
    return md5.hexdigest()


def get_path_dfs_helper(path_collect_list: list, input_path: str, deep: int):
    if not os.path.exists(input_path):
        print(f'目录不存在:{input_path}')
        return
    if deep > 10:
        return
    if os.path.isfile(input_path):
        path_collect_list.append(input_path)
        return
    files = os.listdir(input_path)
    for file in files:
        f_abs = os.path.join(input_path, file)
        get_path_dfs_helper(path_collect_list, f_abs, deep + 1)
    pass


def encrypt_big_file_with_ase256(input_file_path: str, output_file_path: str, key: bytes):
    cipher_config = AES.new(key, mode=AES.MODE_CBC, iv=initial_vector.encode('UTF-8'))
    input_file_total_size = os.path.getsize(input_file_path)
    input_file_read_size = 0
    with open(input_file_path, 'rb') as input_f:
        with open(output_file_path, 'wb+') as output_f:
            while True:
                chunk = input_f.read(FILE_BLOCK_SIZE)
                read_size = len(chunk)
                input_file_read_size += read_size
                if read_size == 0:
                    break
                if input_file_total_size == input_file_read_size:
                    # pad last 16bytes
                    if read_size <= BLOCK_SIZE:
                        encrypt_file_block = cipher_config.encrypt(pad(chunk, BLOCK_SIZE))
                        output_f.write(encrypt_file_block)
                    else:
                        a = int(read_size / FILE_BLOCK_SIZE)
                        b = int((read_size - a * FILE_BLOCK_SIZE) / BLOCK_SIZE)
                        end = a * FILE_BLOCK_SIZE + b * BLOCK_SIZE
                        output_f.write(cipher_config.encrypt(chunk[:end]))
                        output_f.write(cipher_config.encrypt(pad(chunk[end: len(chunk)], BLOCK_SIZE)))
                        pass
                else:
                    encrypt_file_block = cipher_config.encrypt(chunk)
                    output_f.write(encrypt_file_block)
            pass
    pass


def decrypt_big_file_with_ase256(input_file: str, output_file: str, key, skip_bytes: int = 0):
    cipher_config = AES.new(key, mode=AES.MODE_CBC, iv=initial_vector.encode('UTF-8'))
    input_file_total_size = os.path.getsize(input_file)
    input_file_read_size = skip_bytes
    with open(input_file, 'rb') as input_f:
        with open(output_file, 'wb+') as output_f:
            input_f.seek(skip_bytes)
            while True:
                file_block = input_f.read(FILE_BLOCK_SIZE)
                if file_block is None or len(file_block) <= 0:
                    break
                read_size = len(file_block)
                input_file_read_size += read_size
                if input_file_total_size == input_file_read_size:
                    a = int(read_size / FILE_BLOCK_SIZE)
                    b = int((read_size - a * FILE_BLOCK_SIZE) / BLOCK_SIZE)
                    end = a * FILE_BLOCK_SIZE + (b - 1) * BLOCK_SIZE
                    output_f.write(cipher_config.decrypt(file_block[:end]))
                    # only last 16bytes block for unpad
                    output_f.write(unpad(cipher_config.decrypt(file_block[end:len(file_block)]), BLOCK_SIZE))
                    pass
                else:
                    encrypt_file_block = cipher_config.decrypt(file_block)
                    output_f.write(encrypt_file_block)
            pass
    pass


def compare_file(file_one: str, file_two: str):
    with open(file_one, 'rb') as f_one:
        with open(file_two, 'rb') as f_two:
            while True:
                file_block_one = f_one.read(FILE_BLOCK_SIZE)
                file_block_two = f_two.read(FILE_BLOCK_SIZE)
                if file_block_one is None or len(file_block_one) <= 0:
                    break
                if file_block_two is None or len(file_block_two) <= 0:
                    break
                if len(file_block_one) != len(file_block_two):
                    print('读取block不一致')
                    break
                else:
                    data_same = True
                    for i in range(0, len(file_block_one)):
                        if file_block_one[i] != file_block_two[i]:
                            print(f'{i}处数据不一致')
                            data_same = False
                            break
                if not data_same:
                    return
    pass


if __name__ == '__main__':
    print(f'PackedScriptRunOnGithub.py [encrypt|decrypt|decryptRun] filename')
    if len(sys.argv) < 3:
        print('参数错误!!!')
        sys.exit(0)
    # os.system('ls -alR ../..')
    function_name = str(sys.argv[1])
    if function_name not in ('encrypt', 'decrypt', 'decryptRun'):
        print('功能选择错误,只能选择encrypt;decrypt')
        sys.exit(0)
    script_file_name = sys.argv[2]
    print(f'当前脚本的tp_path:{tp_path}')
    base_dir = tp_path.parent

    if function_name == 'encrypt':
        input_script_abs_path = os.path.join(base_dir, script_file_name)
        if os.path.exists(script_file_name):
            input_script_abs_path = script_file_name
        # script_file_name 是绝对路径的时候需要截取文件名
        tp_script_file_name = os.path.basename(input_script_abs_path)
        output_file_abs_path = os.path.join(base_dir.parent, 'f_input', 'encrypt_data', tp_script_file_name)

        if not os.path.exists(Path(output_file_abs_path).parent):
            os.makedirs(Path(output_file_abs_path).parent)
        if isDebug:
            print(output_file_abs_path)
            print(f'加密文件:{script_file_name}-->{output_file_abs_path}')
        encrypt_big_file_with_ase256(input_script_abs_path, output_file_abs_path, get_ase_encrypt_key())

    decrypt_suffix = 'decrypt_script_'
    if function_name == 'decrypt' or function_name == 'decryptRun':
        input_script_abs_path = os.path.join(base_dir, script_file_name)
        if os.path.exists(script_file_name):
            input_script_abs_path = script_file_name
        tp_script_file_name = os.path.basename(input_script_abs_path)
        output_file_abs_path = os.path.join(base_dir, f'{decrypt_suffix}{tp_script_file_name}')
        if isDebug:
            print(f'解密文件:{script_file_name}-->{output_file_abs_path}')
        decrypt_big_file_with_ase256(input_script_abs_path, output_file_abs_path, get_ase_encrypt_key())
        if function_name == 'decryptRun':
            print(f'执行脚本{output_file_abs_path}')
            os.system(f"python {output_file_abs_path}")
            if os.path.exists(output_file_abs_path):
                os.remove(output_file_abs_path)
    pass
