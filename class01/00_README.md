# Class1 宿題
コードがいっぱいでわかりにくいので、一覧を用意しました。
ダウンロードした辞書は **./data/dictionary0.txt**にお願いします。

## 1. Anagramを作る
### ex01-1
- 辞書の名前
    - 元の辞書 -> dic0_name
    - 小文字変換辞書 -> dic_name
- 全通り順列 -> 辞書を二分探索 の方法

せっかくなので、
- 順列生成する関数(my_next_permutation)
- 二分探索する関数(mi_bynary_search)

も作りました。


### ex01-2
- 辞書の名前
    - 小文字変換辞書 -> dic_name
    - ソート辞書 -> sorted_dic_name
- 全てソートされた辞書を使用
    - create_new_dictionary( )が辞書を作る。 


## 2. 全ての文字を使わなくてもよいルールを追加
### ex02-2
- ex01-2を拡張

### ex02-3
- 辞書の名前
    - 小文字変換辞書 -> dic_name
    - ソート辞書 -> sorted_dic_name
- ランレングス圧縮をした辞書を使用
    - run_length(string &s)がランレングス圧縮をする。

## 3. ゲーム用に拡張
### ex03-2
- ex01-2を拡張
- 点数計算してソートする関数(calculate_scores)を追加

