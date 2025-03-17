#!/usr/bin/python3

"""
同じプロセスを2つに分裂させるfork()関数

1. 親プロセスがfork()関数を呼び出す
2. fork()関数は親プロセスのメモリ空間をコピーして子プロセスを生成
3. 親プロセスには子プロセスのPIDが、子プロセスには0が返る

"""

import os, sys

# 親プロセスのメモリ空間をコピーして子プロセスを生成。子プロセスのPIDが返る
ret = os.fork()

if ret == 0:
    # 子プロセス
    print(f"子プロセスのPID: {os.getpid()}, 親プロセスのPID: {os.getppid()}")
    exit()
else:
    # 親プロセス
    print(f"親プロセスのPID: {os.getpid()}, 子プロセスのPID: {ret}")
    exit()
sys.exit(1)