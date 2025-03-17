#!/usr/bin/python3

"""
別のプログラムを起動するexecve()関数

1. execve()関数の呼び出し
1. execve()関数の引数で指定した実行ファイルからプログラムを読み出して、メモリ上に配置するために必要な情報を読み出す
3. 現在のプロセスのメモリ空間を execve() で読み出したプログラムの情報で上書きする
4. 新しいプロセスの最初に実行すべき命令(エントリーポイント)から実行を開始する

"""

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