from collections import deque

LINKS_PATH = 'class04/data/links.txt'
NK_PATH = 'class04/data/nicknames.txt'


class Node:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.follow_users = []

    def follow(self, id):
        self.follow_users.append(id)


# user_idをkey、Nodeのinstanceをvalueとしたdictionaryを作る
def read_sns():
    user_dic = {}
    with open(NK_PATH) as f:
        lines = f.readlines()
        for line in lines:
            id, name = line.strip().split('\t')
            user_dic[int(id)] = Node(int(id), name)

    # follow関係を読み込む
    with open(LINKS_PATH) as f:
        lines = f.readlines()
        for line in lines:
            followee_id, follower_id = line.split('\t')
            user_dic[int(followee_id)].follow(int(follower_id))
    return user_dic


# bfsで探す
def search_bfs(user_map, start_id, target_id):
    queue = deque()
    # start_idがfollowしているidをqueueに入れる
    queue.extend(user_map[start_id].follow_users)
    # すでに探したid
    already_searched = set()

    while len(queue) > 0:
        user = queue.pop()
        already_searched.add(user)
        # 探しているuserならreturnする
        if user == target_id:
            return True
        # 探しているuserでなければ、その人がfollowしている人をqueueに追加
        for new_user in user_map[user].follow_users:
            # しかしalready_searchedに含まれていない人のみ追加
            if new_user not in already_searched:
                queue.append(new_user)
    return False


# dfsで探す
def search_dfs(user_map, start_id, target_id):
    # start_idがfollowしているidをstackに入れる
    stack = user_map[start_id].follow_users
    # すでに探したid
    already_searched = set()

    while len(stack) > 0:
        user = stack.pop()
        already_searched.add(user)
        # 探しているuserならreturnする
        if user == target_id:
            return True
        # 探しているuserでなければ、その人がfollowしている人をqueueに追加
        for new_user in user_map[user].follow_users:
            # しかしalready_searchedに含まれていない人のみ追加
            if new_user not in already_searched:
                stack.append(new_user)
    return False


if __name__ == '__main__':
    user_dic = read_sns()

    # adrian から eugene
    result = search_bfs(user_dic, 1, 25)
    # dfsで探索
    # result = search_dfs(user_map, 1, 25)

    if result:
        print('Found!')
    else:
        print('Not Found!')
