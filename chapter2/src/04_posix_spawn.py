import os

os.posix_spawn("/bin/echo", ["echo", "posix_spawn()によって生成されました"], {})
print("echo コマンドを生成しました")