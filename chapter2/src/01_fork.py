#!/usr/bin/python3

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