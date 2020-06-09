import heapq
EDGES_PATH = 'class04/data/station/edges.txt'
STATION_PATH = 'class04/data/station/stations.txt'

# ダイクストラ法で任意の駅間の距離を調べる


class Station:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        # 駅数分だけinfで初期化
        self.adjacent = []

    def add_edge(self, id, time):
        # (所要時間, 駅id)
        self.adjacent.append((time, id))

    def print(self):
        print(f'{self.id}: {self.name}')
        print(self.adjacent)


def read_route():
    station_dic = {}
    # 駅のidをkey、Stationのinstanceをvalueとしたdictionaryを作る
    with open(STATION_PATH) as f:
        lines = f.readlines()
        for line in lines:
            id, name = line.strip().split('\t')
            station_dic[int(id)] = Station(int(id), name)

    # 駅の所要時間を格納
    with open(EDGES_PATH) as f:
        lines = f.readlines()
        for line in lines:
            # 駅x 駅y 所要時間
            x, y, time = line.strip().split('\t')
            station_dic[int(x)].add_edge(int(y), int(time))
            station_dic[int(y)].add_edge(int(x), int(time))
    return station_dic


def dijkstra(station_dic, start, end):
    # 駅数
    length = len(station_dic)
    # start地点からかかる時間
    cost = [float('inf')] * length
    # start地点は0
    cost[start] = 0

    # 探索状況
    # WHITE: 未探索 ・ GRAY: 未確定 ・ BLACK: 確定
    color = ['WHITE'] * length
    # start地点は探索したが未確定
    color[start] = 'GRAY'

    # 経路
<< << << < HEAD
    path = [[]] * length
    # start地点
    path[start].append(station_dic[start].name)
== == == =
    path = [''] * length
    # start地点
    path[start] = station_dic[start].name
>>>>>> > 01098432ceb743e5edd7f2ffe9125fcfc8b92393

    # start地点を優先度つきキューに
    # これで最初にstart地点が取り出される
    # (所要時間, start地点のid)
    pq = [(0, start)]
    heapq.heapify(pq)

    # pqが空ではない
    while pq:
        # 1番所要時間が短い駅
        minstation = heapq.heappop(pq)

        # 探している駅なら返す
        if minstation[1] == end:
            return path[end]

        # 確定
        color[minstation[1]] = 'BLACK'

        # 最小値が最短でなければ無視
        if cost[minstation[1]] < minstation[0]:
            continue

        # minstationに隣接するリストが存在する限り
        for next_station in station_dic[minstation[1]].adjacent:
            if color[next_station[1]] != 'BLACK':
                new_cost = cost[minstation[1]] + next_station[0]
                # costがminstationを経由する方が近い時
                if new_cost < cost[next_station[1]]:
                    cost[next_station[1]] = new_cost
                    color[next_station[1]] = 'GRAY'
                    # 経路を更新
                    path[next_station[1]] = path[minstation[1]] + \
<< << << < HEAD
                        [station_dic[next_station[1]].name]
== == == =
                        ' -> ' + station_dic[next_station[1]].name
>>>>>> > 01098432ceb743e5edd7f2ffe9125fcfc8b92393
                    heapq.heappush(pq, (new_cost, next_station[1]))

    return 'Not Found'


if __name__ == '__main__':
    station_dic = read_route()

    path = dijkstra(station_dic, 249, 1)

<<<<<<< HEAD
    print(' -> '.join(path))
=======
    print(path)
>>>>>>> 01098432ceb743e5edd7f2ffe9125fcfc8b92393
