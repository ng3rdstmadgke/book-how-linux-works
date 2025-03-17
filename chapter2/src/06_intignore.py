import signal

def handler(signum: int, frame):
    signame = signal.Signals(signum).name
    print(f"signal {signame} ({signum}) received.")


# SIGINTを無視するように設定
#   signalnum: ハンドラを設定するシグナル番号
#   handler: シグナルを受信したときの処理を定義するハンドラ
#            関数以外にも以下の値を指定できる
#            - signal.SIG_IGN: シグナルを無視するハンドラ
#            - signal.SIG_DFL: シグナルのデフォルトのハンドラ
signal.signal(
    signalnum=signal.SIGINT,
    handler=handler,
)
while True:
    pass