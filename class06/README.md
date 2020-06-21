# Malloc Challenge 2020
Sora Tagami

## How to run
```shell
cd class06
make
```
my_linked_list_malloc.cが、my_mallocのファイルです。

## 工夫した点
- Free Listをアドレス順に持っておく。
- 新しくfreeしたら、空き領域が連続しているところを統合する。(1.はこれをやりやすくするための操作)
- metadataのサイズよりも小さい部分は使われなくなってしまうので、これも統合する。

- デバッグ用にfree listを出力する、print_free_list()関数を用意しました。
    - サイズ
    - アドレス
    - 次の要素のアドレス
    - 合計空き容量


## Document
https://docs.google.com/presentation/d/1oizL65Rw8Gtc2lIAg8gg3BIpTyCZWk3fR3d5zkJvvW4/edit?usp=sharing

実行すると、テストケースの結果が出力されますが、このスライドの図と対応しています。