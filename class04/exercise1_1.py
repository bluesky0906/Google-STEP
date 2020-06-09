from collections import deque

<<<<<<< HEAD
LINKS_PATH = 'class04/data//sns/links.txt'
NK_PATH = 'class04/data/sns/nicknames.txt'
=======
LINKS_PATH = 'class04/data/links.txt'
NK_PATH = 'class04/data/nicknames.txt'
>>>>>>> 01098432ceb743e5edd7f2ffe9125fcfc8b92393


class Node:
    def __init__(self, id, name):
        self.id = id
        self.name = name
<<<<<<< HEAD
        self.linked_nodes = []

    def link(self, id):
        self.linked_nodes.append(id)


# idをkey、Nodeのinstanceをvalueとしたdictionaryを作る
def read_links(node_path, links_path):
    dic = {}
    with open(node_path) as f:
        lines = f.readlines()
        for line in lines:
            id, name = line.strip().split('\t')
            dic[int(id)] = Node(int(id), name)

    # link関係を読み込む
    with open(links_path) as f:
        lines = f.readlines()
        for line in lines:
            from_id, to_id = line.split('\t')
            dic[int(from_id)].link(int(to_id))
    return dic


# 名前からidをひく関数
def name_to_id(dic, name):
    for node in dic.values():
        if node.name == name:
            return node.id


# bfsで探す
def search_bfs(dic, start_id, target_id):
    queue = deque()
    # start_idがlinkしているidをqueueに入れる
    queue.extend(dic[start_id].linked_nodes)
    # すでに探したid
    already_searched = set()

    # 通ってきたリンク先
    path = []

    while len(queue) > 0:
        id = queue.pop()
        already_searched.add(id)
        path.append(id)
        # 探しているidならreturnする
        if id == target_id:
            return path
        # 探しているuserでなければ、その人がlinkしているidをqueueに追加
        for new_id in dic[id].linked_nodes:
            # しかしalready_searchedに含まれていないidのみ追加
            if new_id not in already_searched:
                queue.append(new_id)
=======
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
>>>>>>> 01098432ceb743e5edd7f2ffe9125fcfc8b92393
    return False


# dfsで探す
<<<<<<< HEAD
def search_dfs(dic, start_id, target_id):
    # start_idがlinkしているidをstackに入れる
    stack = dic[start_id].linked_nodes
    # すでに探したid
    already_searched = set()

    # 通ってきたリンク先
    path = []

    while len(stack) > 0:
        id = stack.pop()
        already_searched.add(id)
        path.append(id)
        # 探しているidならreturnする
        if id == target_id:
            return path
        # 探しているidでなければ、その人がlinkしているidをqueueに追加
        for new_id in dic[id].linked_nodes:
            # しかしalready_searchedに含まれていないidのみ追加
            if new_id not in already_searched:
                stack.append(new_id)
=======
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
>>>>>>> 01098432ceb743e5edd7f2ffe9125fcfc8b92393
    return False


if __name__ == '__main__':
<<<<<<< HEAD
    user_dic = read_links(NK_PATH, LINKS_PATH)

    # adrian から eugene
    start_id = name_to_id(user_dic, 'adrian')
    target_id = name_to_id(user_dic, 'eugene')
    result = search_bfs(user_dic, start_id, target_id)
    # dfsで探索
    # result = search_dfs(user_map, start_id, target_id)

    if result:
        print('Found!')
        result_name = [user_dic[r].name for r in result]
        print(' -> '.join(result_name))
=======
    user_dic = read_sns()

    # adrian から eugene
    result = search_bfs(user_dic, 1, 25)
    # dfsで探索
    # result = search_dfs(user_map, 1, 25)

    if result:
        print('Found!')
>>>>>>> 01098432ceb743e5edd7f2ffe9125fcfc8b92393
    else:
        print('Not Found!')
