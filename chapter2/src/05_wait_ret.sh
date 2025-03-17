#!/bin/bash

false &
wait $! # falseプロセスの終了を待つ。falseコマンドのPIDは$!変数で取得できる
echo "false コマンドが終了しました: $?" # wait後にfalseプロセスの戻り値は$?変数で取得できる