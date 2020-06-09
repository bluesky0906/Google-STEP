from exercise1_1 import search_bfs, read_links, NK_PATH, LINKS_PATH

# 全ての組み合わせの二人について、つながっている確率とつながっていない確率
# またつながってない組み合わせ

if __name__ == '__main__':
    user_dic = read_links(NK_PATH, LINKS_PATH)
    length = len(user_dic)

    not_connecting = []
    results = []
    for id, user in user_dic.items():
        for id2, user2 in user_dic.items():
            # 同じ人の時
            if id == id2:
                continue
            result = search_bfs(user_dic, id, id2)
            # つながっていない組み合わせが見つかったら
            if not result:
                not_connecting.append('{} -> {}'.format(user.name, user2.name))
            results.append(result)

    # つながっている確率とつながっていない確率
    false = results.count(False)
    true = results.count(True)
    total = len(results)
    print(f'connecting: {true/total * 100} %')
    print(f'not connecting: {false/total * 100} %')

    # つながっていない組み合わせ
    print('Not connecting list: ', not_connecting)
