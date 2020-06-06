from collections import deque

links_path = 'class04/data/links.txt'
nk_path = 'class04/data/nicknames.txt'


class Node:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.follow_users = []

    def follow(self, id):
        self.follow_users.append(id)


# bfsで探す
def search_bfs(start_id, target_id):
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
            print('Found!')
            return True
        # 探しているuserでなければ、その人がfollowしている人をqueueに追加
        for new_user in user_map[user].follow_users:
            # しかしalready_searchedに含まれていない人のみ追加
            if new_user not in already_searched:
                queue.append(new_user)
    print('Not Found!')
    return False


if __name__ == '__main__':
    # user_idをkey、Nodeのinstanceをvalueとしたmapを作る
    user_map = {}
    with open(nk_path) as f:
        lines = f.readlines()
        for line in lines:
            id, name = line.split('\t')
            user_map[int(id)] = Node(int(id), name)

    # follow関係を読み込む
    with open(links_path) as f:
        lines = f.readlines()
        for line in lines:
            followee_id, follower_id = line.split('\t')
            user_map[int(followee_id)].follow(int(follower_id))

    # adrian から eugene
    search_bfs(1, 25)
