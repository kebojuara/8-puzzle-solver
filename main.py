import heapq
import math
import time

dx = [-1, 1, 0, 0]
dy = [0, 0, 1, -1]

goal_state = "123456780"

def setGoalState(state):
    global goal_state
    goal_state = state


euclid_counter = manhattan_counter = 0
tiles_out_of_place_counter = 0
gbfs_manhattan_counter = gbfs_euclid_counter = 0
gbfs_tiles_out_of_place_counter = 0

euclid_path = manhattan_path = []
tiles_out_of_place_path = []
gbfs_manhattan_path = gbfs_euclid_path = []
gbfs_tiles_out_of_place_path = []

euclid_cost = manhattan_cost = 0
tiles_out_of_place_cost = 0
gbfs_manhattan_cost = gbfs_euclid_cost = 0
gbfs_tiles_out_of_place_cost = 0

euclid_depth = manhattan_depth = 0
tiles_out_of_place_depth = 0
gbfs_manhattan_depth = 0
gbfs_euclid_depth = 0
gbfs_tiles_out_of_place_depth = 0

time_euclid = 0
time_manhattan = 0
time_tiles_out_of_place = 0
time_gbfs_manhattan = 0
time_gbfs_euclid = 0
time_gbfs_tiles_out_of_place = 0


def getStringRepresentation(x):
    return str(x).zfill(9)


def getChildren(state):
    children = []
    idx = state.index('0')
    i, j = divmod(idx, 3)
    for k in range(4):
        nx, ny = i + dx[k], j + dy[k]
        if checkValid(nx, ny):
            nwIdx = nx * 3 + ny
            listTemp = list(state)
            listTemp[idx], listTemp[nwIdx] = listTemp[nwIdx], listTemp[idx]
            children.append(''.join(listTemp))
    return children


def getPath(parentMap, inputState):
    path = []
    temp = int(goal_state)
    initial_state_int = int(inputState)

    while temp != initial_state_int:
        path.append(temp)
        if temp not in parentMap:
            return []
        temp = parentMap[temp]

    path.append(initial_state_int)
    path.reverse()
    return path


def printPath(path):
    for i in path:
        print(getStringRepresentation(i))


def goalTest(state):
    return getStringRepresentation(state) == goal_state


def isSolvable(digit):
    count = 0
    for i in range(0, 9):
        for j in range(i, 9):
            if digit[i] > digit[j] and digit[i] != 9:
                count += 1
    return count % 2 == 0


def checkValid(i, j):
    return 0 <= i < 3 and 0 <= j < 3


def getManhattanDistance(state):
    tot = 0
    global goal_state
    for i in range(1, 9):
        goal_idx = goal_state.index(str(i))
        goalX, goalY = divmod(goal_idx, 3)
        idx = state.index(str(i))
        itemX, itemY = divmod(idx, 3)
        tot += abs(goalX - itemX) + abs(goalY - itemY)
    return tot


def getEuclideanDistance(state):
    tot = 0
    global goal_state
    for i in range(1, 9):
        goal_idx = goal_state.index(str(i))
        goalX, goalY = divmod(goal_idx, 3)
        idx = state.index(str(i))
        itemX, itemY = divmod(idx, 3)
        tot += math.sqrt((goalX - itemX) ** 2 + (goalY - itemY) ** 2)
    return tot


def getTilesOutOfPlace(state):
    misplaced_tiles = 0
    global goal_state
    for i in range(9):
        if state[i] != '0' and state[i] != goal_state[i]:
            misplaced_tiles += 1
    return misplaced_tiles


def AStarSearch_manhattan(inputState):
    start_time = time.time()
    integer_state = int(inputState)
    heap = []
    explored = {}
    parent = {}
    cost_map = {}
    heapq.heappush(heap, (getManhattanDistance(inputState), integer_state))
    cost_map[integer_state] = getManhattanDistance(inputState)
    heap_map = {integer_state: 1}
    global manhattan_counter, manhattan_path, manhattan_cost, manhattan_depth, time_manhattan
    manhattan_depth = 0
    while heap:
        node = heapq.heappop(heap)
        state = node[1]
        string_state = getStringRepresentation(state)
        parent_cost = node[0] - getManhattanDistance(string_state)
        if not state in explored:
            manhattan_depth = max(parent_cost, manhattan_depth)
        explored[state] = 1
        if goalTest(state):
            path = getPath(parent, inputState)
            manhattan_path = path
            manhattan_counter = len(explored)
            manhattan_cost = len(path) - 1
            time_manhattan = float(time.time() - start_time)
            return 1
        children = getChildren(string_state)
        for child in children:
            new_cost = getManhattanDistance(child)
            child_int = int(child)
            if child_int not in explored and child_int not in heap_map:
                heapq.heappush(heap, (parent_cost + new_cost + 1, child_int))
                heap_map[child_int] = 1
                cost_map[child_int] = parent_cost + new_cost + 1
                parent[child_int] = state
            elif child_int in heap_map:
                if (new_cost + parent_cost + 1) < cost_map[child_int]:
                    parent[child_int] = state
                    cost_map[child_int] = new_cost + parent_cost + 1
                    heapq.heappush(heap, (parent_cost + 1 + new_cost, child_int))
    manhattan_cost = 0
    manhattan_path = []
    manhattan_counter = len(explored)
    time_manhattan = float(time.time() - start_time)
    return 0


def AStarSearch_euclid(inputState):
    start_time = time.time()
    integer_state = int(inputState)
    heap = []
    explored = {}
    parent = {}
    cost_map = {}
    heapq.heappush(heap, (getEuclideanDistance(inputState), integer_state))
    cost_map[integer_state] = getEuclideanDistance(inputState)
    heap_map = {integer_state: 1}
    global euclid_counter, euclid_path, euclid_cost, euclid_depth, time_euclid
    euclid_depth = 0
    while heap:
        node = heapq.heappop(heap)
        state = node[1]
        string_state = getStringRepresentation(state)
        parent_cost = node[0] - getEuclideanDistance(string_state)
        if not state in explored:
            euclid_depth = max(parent_cost, euclid_depth)
        explored[state] = 1
        if goalTest(state):
            path = getPath(parent, inputState)
            euclid_path = path
            euclid_counter = len(explored)
            euclid_cost = len(path) - 1
            time_euclid = float(time.time() - start_time)
            return 1
        children = getChildren(string_state)
        for child in children:
            new_cost = getEuclideanDistance(child)
            child_int = int(child)
            if child_int not in explored and child_int not in heap_map:
                heapq.heappush(heap, (parent_cost + new_cost + 1, child_int))
                heap_map[child_int] = 1
                cost_map[child_int] = parent_cost + new_cost + 1
                parent[child_int] = state
            elif child_int in heap_map:
                if (new_cost + parent_cost + 1) < cost_map[child_int]:
                    parent[child_int] = state
                    cost_map[child_int] = new_cost + parent_cost + 1
                    heapq.heappush(heap, (parent_cost + 1 + new_cost, child_int))
    euclid_cost = 0
    euclid_path = []
    euclid_counter = len(explored)
    time_euclid = float(time.time() - start_time)
    return 0


def AStarSearch_tiles_out_of_place(inputState):
    start_time = time.time()
    integer_state = int(inputState)
    heap = []
    explored = {}
    parent = {}
    cost_map = {}
    heapq.heappush(heap, (getTilesOutOfPlace(inputState), integer_state))
    cost_map[integer_state] = getTilesOutOfPlace(inputState)
    heap_map = {integer_state: 1}
    global tiles_out_of_place_counter, tiles_out_of_place_path, tiles_out_of_place_cost, tiles_out_of_place_depth, time_tiles_out_of_place
    tiles_out_of_place_depth = 0
    while heap:
        node = heapq.heappop(heap)
        state = node[1]
        string_state = getStringRepresentation(state)
        parent_cost = node[0] - getTilesOutOfPlace(string_state)
        if not state in explored:
            tiles_out_of_place_depth = max(parent_cost, tiles_out_of_place_depth)
        explored[state] = 1
        if goalTest(state):
            path = getPath(parent, inputState)
            tiles_out_of_place_path = path
            tiles_out_of_place_counter = len(explored)
            tiles_out_of_place_cost = len(path) - 1
            time_tiles_out_of_place = float(time.time() - start_time)
            return 1
        children = getChildren(string_state)
        for child in children:
            new_cost = getTilesOutOfPlace(child)
            child_int = int(child)
            if child_int not in explored and child_int not in heap_map:
                heapq.heappush(heap, (parent_cost + new_cost + 1, child_int))
                heap_map[child_int] = 1
                cost_map[child_int] = parent_cost + new_cost + 1
                parent[child_int] = state
            elif child_int in heap_map:
                if (new_cost + parent_cost + 1) < cost_map[child_int]:
                    parent[child_int] = state
                    cost_map[child_int] = new_cost + parent_cost + 1
                    heapq.heappush(heap, (parent_cost + 1 + new_cost, child_int))
    tiles_out_of_place_cost = 0
    tiles_out_of_place_path = []
    tiles_out_of_place_counter = len(explored)
    time_tiles_out_of_place = float(time.time() - start_time)
    return 0


def GreedyBestFirstSearch_manhattan(inputState):
    start_time = time.time()
    integer_state = int(inputState)
    heap = []
    explored = {}
    parent = {}
    g_cost_map = {}
    h_n = getManhattanDistance(inputState)
    heapq.heappush(heap, (h_n, integer_state))
    g_cost_map[integer_state] = 0
    global gbfs_manhattan_counter, gbfs_manhattan_path, gbfs_manhattan_cost, gbfs_manhattan_depth, time_gbfs_manhattan
    gbfs_manhattan_depth = 0
    while heap:
        node = heapq.heappop(heap)
        state = node[1]
        string_state = getStringRepresentation(state)
        if state in explored:
            continue
        explored[state] = 1
        current_g_cost = g_cost_map[state]
        gbfs_manhattan_depth = max(gbfs_manhattan_depth, current_g_cost)
        if goalTest(state):
            path = getPath(parent, inputState)
            gbfs_manhattan_path = path
            gbfs_manhattan_counter = len(explored)
            gbfs_manhattan_cost = len(path) - 1
            time_gbfs_manhattan = float(time.time() - start_time)
            return 1
        children = getChildren(string_state)
        for child in children:
            child_int = int(child)
            if child_int not in explored:
                h_n_child = getManhattanDistance(child)
                heapq.heappush(heap, (h_n_child, child_int))
                parent[child_int] = state
                g_cost_map[child_int] = current_g_cost + 1
    gbfs_manhattan_cost = 0
    gbfs_manhattan_path = []
    gbfs_manhattan_counter = len(explored)
    time_gbfs_manhattan = float(time.time() - start_time)
    return 0


def GreedyBestFirstSearch_euclid(inputState):
    start_time = time.time()
    integer_state = int(inputState)
    heap = []
    explored = {}
    parent = {}
    g_cost_map = {}
    h_n = getEuclideanDistance(inputState)
    heapq.heappush(heap, (h_n, integer_state))
    g_cost_map[integer_state] = 0
    global gbfs_euclid_counter, gbfs_euclid_path, gbfs_euclid_cost, gbfs_euclid_depth, time_gbfs_euclid
    gbfs_euclid_depth = 0
    while heap:
        node = heapq.heappop(heap)
        state = node[1]
        string_state = getStringRepresentation(state)
        if state in explored:
            continue
        explored[state] = 1
        current_g_cost = g_cost_map[state]
        gbfs_euclid_depth = max(gbfs_euclid_depth, current_g_cost)
        if goalTest(state):
            path = getPath(parent, inputState)
            gbfs_euclid_path = path
            gbfs_euclid_counter = len(explored)
            gbfs_euclid_cost = len(path) - 1
            time_gbfs_euclid = float(time.time() - start_time)
            return 1
        children = getChildren(string_state)
        for child in children:
            child_int = int(child)
            if child_int not in explored:
                h_n_child = getEuclideanDistance(child)
                heapq.heappush(heap, (h_n_child, child_int))
                parent[child_int] = state
                g_cost_map[child_int] = current_g_cost + 1
    gbfs_euclid_cost = 0
    gbfs_euclid_path = []
    gbfs_euclid_counter = len(explored)
    time_gbfs_euclid = float(time.time() - start_time)
    return 0


def GreedyBestFirstSearch_tiles_out_of_place(inputState):
    start_time = time.time()
    integer_state = int(inputState)
    heap = []
    explored = {}
    parent = {}
    g_cost_map = {}
    h_n = getTilesOutOfPlace(inputState)
    heapq.heappush(heap, (h_n, integer_state))
    g_cost_map[integer_state] = 0
    global gbfs_tiles_out_of_place_counter, gbfs_tiles_out_of_place_path, gbfs_tiles_out_of_place_cost, gbfs_tiles_out_of_place_depth, time_gbfs_tiles_out_of_place
    gbfs_tiles_out_of_place_depth = 0
    while heap:
        node = heapq.heappop(heap)
        state = node[1]
        string_state = getStringRepresentation(state)
        if state in explored:
            continue
        explored[state] = 1
        current_g_cost = g_cost_map[state]
        gbfs_tiles_out_of_place_depth = max(gbfs_tiles_out_of_place_depth, current_g_cost)
        if goalTest(state):
            path = getPath(parent, inputState)
            gbfs_tiles_out_of_place_path = path
            gbfs_tiles_out_of_place_counter = len(explored)
            gbfs_tiles_out_of_place_cost = len(path) - 1
            time_gbfs_tiles_out_of_place = float(time.time() - start_time)
            return 1
        children = getChildren(string_state)
        for child in children:
            child_int = int(child)
            if child_int not in explored:
                h_n_child = getTilesOutOfPlace(child)
                heapq.heappush(heap, (h_n_child, child_int))
                parent[child_int] = state
                g_cost_map[child_int] = current_g_cost + 1
    gbfs_tiles_out_of_place_cost = 0
    gbfs_tiles_out_of_place_path = []
    gbfs_tiles_out_of_place_counter = len(explored)
    time_gbfs_tiles_out_of_place = float(time.time() - start_time)
    return 0