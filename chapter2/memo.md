2章 プロセス管理 (基礎編)
---

# 同じプロセスを2つに分裂させるfork()関数

1. 親プロセスがfork()関数を呼び出す
2. fork()関数は親プロセスのメモリ空間をコピーして子プロセスを生成
3. 親プロセスには子プロセスのPIDが、子プロセスには0が返る

```bash
python3 chapter2/src/01_fork.py 
# 親プロセスのPID: 3449532, 子プロセスのPID: 3449533
# 子プロセスのPID: 3449533, 親プロセスのPID: 3449532
```

<img width="700px" src="./img/01_fork.png">

# 別のプログラムを起動するexecve()関数

1. execve()関数の呼び出し
2. execve()関数の引数に指定した実行ファイルからプログラムを読み出して、メモリ上に配置するために必要な情報を読み出す
3. 現在のプロセスのメモリ空間を読み出したプログラムの情報で上書きする
4. 新しいプロセスの最初に実行すべき命令(エントリーポイント)から実行を開始する


```bash
python3 chapter2/src/02_fork_and_exec.py
# 親プロセスのPID: 3452642, 子プロセスのPID: 3452643
# 子プロセスのPID: 3452643, 親プロセスのPID: 3452642
# PID=3452643 からこんにちは
```

<img width="700px" src="./img/03_fork_and_exec.png">

## 実行ファイルのフォーマット


execve()関数の実現のために、実行ファイルはプログラムのコードやデータに加えて次のようなプログラムの起動に必要なデータを保持しています

- コード領域のファイル上オフセット、サイズ、及びメモリマップ開始アドレス
- データ領域についての上記と同じ情報
- 最初に実行する命令のメモリアドレス

Linuxの実行ファイルがこれらの情報をどのように保持しているのかについて見てみましょう。  
Linuxの実行ファイルは通常**Executable and Linking Format(ELF)**というフォーマットになっています。  
ELFの各種情報は `readelf` コマンドで確認することができます。


```bash
# --no-pie:
#   PIE（Position Independent Executable）を無効にする
#   PIEが有効になっているとメモリ上のロードアドレスがランダム化される
$ cc -o chapter2/dst/pause -no-pie chapter2/src/03_pause.c
```

プログラムの開始アドレスを取得するには `readelf -h` を実行します。  
"Entry point address" の `0x401050` がこのプログラムのエントリポイントになります。

```bash

# -h --file-header: ファイルヘッダオプション
readelf -h chapter2/dst/pause
# ELF Header:
#   Magic:   7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00 
#   Class:                             ELF64
#   Data:                              2's complement, little endian
#   Version:                           1 (current)
#   OS/ABI:                            UNIX - System V
#   ABI Version:                       0
#   Type:                              EXEC (Executable file)
#   Machine:                           Advanced Micro Devices X86-64
#   Version:                           0x1
#   Entry point address:               0x401050
#   Start of program headers:          64 (bytes into file)
#   Start of section headers:          13912 (bytes into file)
#   Flags:                             0x0
#   Size of this header:               64 (bytes)
#   Size of program headers:           56 (bytes)
#   Number of program headers:         13
#   Size of section headers:           64 (bytes)
#   Number of section headers:         31
#   Section header string table index: 30
```

コードとデータのファイル内オフセット、サイズ、開始アドレスを取得するにはは `readelf -S` を実行します。
`.text` がコード領域、 `.data` がデータ領域となります。



```bash
# -S --section-headers: セクションヘッダオプション
readelf -S chapter2/dst/pause
# There are 31 section headers, starting at offset 0x3658:
# 
# Section Headers:
#   [Nr] Name              Type             Address           Offset
#        Size              EntSize          Flags  Link  Info  Align
# ...
#   [15] .text             PROGBITS         0000000000401050  00001050
#        00000000000000fa  0000000000000000  AX       0     0     16
# ...
#   [25] .data             PROGBITS         0000000000404020  00003020
#        0000000000000010  0000000000000000  WA       0     0     8
# ...
# Key to Flags:
#   W (write), A (alloc), X (execute), M (merge), S (strings), I (info),
#   L (link order), O (extra OS processing required), G (group), T (TLS),
#   C (compressed), x (unknown), o (OS specific), E (exclude),
#   D (mbind), l (large), p (processor specific)
```

### まとめ

- 実行ファイルは複数の領域に分けられており、それぞれを**セクション**と呼ぶ
- セクションの情報は2行を1組として表示される
- 数値はすべて16進数
- セクションの主な情報
  - `Name` : セクション名 (`.text`=コードセクション, `.data`=データセクション)
  - `Address` : メモリマップ開始アドレス
  - `Offset` : ファイル内オフセット
  - `Size` : サイズ


| 項目 | コードセクション | データセクション |
| --- | --- | --- |
| メモリマップの開始アドレス | `401050` | `404020` |
| サイズ | `fa` | `10` |
| ファイル内オフセット | `1050` | `3020` |


## メモリマップを確認する

プログラムから作成したプロセスのメモリマップは `/proc/<pid>/maps` というファイルから確認できます。  
コード領域、データ領域の「メモリマップの開始アドレス ~ サイズ」がメモリマップの範囲内に収まっていることがわかります。



```bash
./chapter2/dst/pause &
# [1] 3482917
cat /proc/3482917/maps
# 00400000-00401000 r--p 00000000 103:01 9844161           /home/ubuntu/Projects/book-how-linux-works/chapter2/dst/pause
# 00401000-00402000 r-xp 00001000 103:01 9844161           /home/ubuntu/Projects/book-how-linux-works/chapter2/dst/pause  ★ コード領域
# 00402000-00403000 r--p 00002000 103:01 9844161           /home/ubuntu/Projects/book-how-linux-works/chapter2/dst/pause
# 00403000-00404000 r--p 00002000 103:01 9844161           /home/ubuntu/Projects/book-how-linux-works/chapter2/dst/pause
# 00404000-00405000 rw-p 00003000 103:01 9844161           /home/ubuntu/Projects/book-how-linux-works/chapter2/dst/pause  ★ データ領域
# 7fc891400000-7fc891428000 r--p 00000000 103:01 12186     /usr/lib/x86_64-linux-gnu/libc.so.6
# 7fc891428000-7fc8915bd000 r-xp 00028000 103:01 12186     /usr/lib/x86_64-linux-gnu/libc.so.6
# 7fc8915bd000-7fc891615000 r--p 001bd000 103:01 12186     /usr/lib/x86_64-linux-gnu/libc.so.6
# 7fc891615000-7fc891616000 ---p 00215000 103:01 12186     /usr/lib/x86_64-linux-gnu/libc.so.6
# 7fc891616000-7fc89161a000 r--p 00215000 103:01 12186     /usr/lib/x86_64-linux-gnu/libc.so.6
# 7fc89161a000-7fc89161c000 rw-p 00219000 103:01 12186     /usr/lib/x86_64-linux-gnu/libc.so.6
# 7fc89161c000-7fc891629000 rw-p 00000000 00:00 0 
# 7fc89162c000-7fc89162f000 rw-p 00000000 00:00 0 
# 7fc891636000-7fc891638000 rw-p 00000000 00:00 0 
# 7fc891638000-7fc89163a000 r--p 00000000 103:01 12182     /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
# 7fc89163a000-7fc891664000 r-xp 00002000 103:01 12182     /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
# 7fc891664000-7fc89166f000 r--p 0002c000 103:01 12182     /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
# 7fc891670000-7fc891672000 r--p 00037000 103:01 12182     /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
# 7fc891672000-7fc891674000 rw-p 00039000 103:01 12182     /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
# 7ffc92d1d000-7ffc92d3e000 rw-p 00000000 00:00 0          [stack]
# 7ffc92d4c000-7ffc92d50000 r--p 00000000 00:00 0          [vvar]
# 7ffc92d50000-7ffc92d52000 r-xp 00000000 00:00 0          [vdso]
# ffffffffff600000-ffffffffff601000 --xp 00000000 00:00 0  [vsyscall]
```