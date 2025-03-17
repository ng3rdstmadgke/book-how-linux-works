#!/usr/bin/python3

import os, sys

# 親プロセスのメモリ空間をコピーして子プロセスを生成
ret = os.fork()

if ret == 0:
    # 子プロセス
    print(f"子プロセスのPID: {os.getpid()}, 親プロセスのPID: {os.getppid()}")
    # 子プロセスのメモリ空間を /bin/echo で上書き
    os.execve("/bin/echo", ["echo", f"PID={os.getpid()} からこんにちは"], {})
    exit()
else:
    # 親プロセス
    print(f"親プロセスのPID: {os.getpid()}, 子プロセスのPID: {ret}")
    exit()
sys.exit(1)