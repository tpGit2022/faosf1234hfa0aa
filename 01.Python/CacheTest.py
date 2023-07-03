import os
import shutil
import time
from pathlib import Path
from datetime import datetime

tp_path = Path(os.path.abspath(__file__))
file_store_abs_path = os.path.abspath(__file__)


def get_path_dfs_helper(path_collect_list: list, input_path: str, deep: int):
    if not os.path.exists(input_path):
        print(f'目录不存在:{input_path}')
        return
    if deep > 20:
        return
    if os.path.isfile(input_path):
        path_collect_list.append(input_path)
        return
    files = os.listdir(input_path)
    for f in files:
        f_abs = os.path.join(input_path, f)
        get_path_dfs_helper(path_collect_list, f_abs, deep + 1)
    pass


def check_cache():
    file_path_list = []
    print(tp_path)
    print(file_store_abs_path)
    cache_dir = os.path.join(tp_path.parent.parent, 'Cache')
    get_path_dfs_helper(file_path_list, cache_dir, 0)
    print(file_path_list)
    test_cache = os.path.join(cache_dir, 'data.cache')
    with open(test_cache, 'w+', encoding="UTF-8") as f:
        now = datetime.now()
        # 转换为本地时间字符串
        local_time_str = now.strftime('%Y-%m-%d %H:%M:%S')
        input_str = f"{time.time()}->{local_time_str}"
        f.write(input_str)
    pass


if __name__ == '__main__':
    check_cache()
    pass