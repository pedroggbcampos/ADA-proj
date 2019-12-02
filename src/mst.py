#!/usr/bin/env python3

import sys
import random
import math
import collections

# False when you submit to kattis
# DEBUG = True
DEBUG = False

N = 0
W = 0
E = 0.0
s = 0
parent = dict()
rank = dict()

NEIGHBOR_DICT = {}


def approx_mst_weight():

    # if (N < 1000 and E < 0.1):
    #     return kruskalAlgorithm()

    estimators_sum = 0
    i = 1
    approx_cc = 0
    while (i < W):
        approx_cc = approx_connected_comps(i)
        estimators_sum += approx_cc
        # if (approx_cc < 1.5):
        #     estimators_sum += W-i-1
        #     break
        i += 1

    # This queries Kattis more than needed, this can be optimized
    # There are floating point points, hence it queries too much
    # Maybe write a special method just for this last approximation?
    last_acc = approx_connected_comps(W)
    # if (last_acc > 7):
    #     estimators_sum += (last_acc)
    #     estimators_sum -= 1
    #     estimators_sum -= (last_acc-1)*(W+1)
    return N - W + estimators_sum - (W * (last_acc-1))


def approx_connected_comps(subgraph_weight):

    # 4 has given the best results so far, but there may exist a better number
    # s = min(math.ceil(4.25/(E**2)), N)  # choose s
    # s = N/100
    # s = math.ceil(6/(E**2))  # choose s
    bi_sum = 0
    i = 1
    # nodes_visited = [-1]
    # nodes = random.shuffle(list(range(N)))
    while (i < s):
        # choose X according to Pr[X ≥ k] = 1/k : X = 1/rand(0, 1) behaves like this : for example, P(1/rand(0,1) >= 2 ) = 1/2
        x = 1/random.uniform(0, 1)

        # node_in_comp = False

        # node = -1
        # while node in nodes_visited:
        node = random.randint(0, N-1)
        # nodes_visited.append(node)

        # node = nodes[i]
        bi_sum += bfs(node, subgraph_weight, min(math.floor(x), 500))
        i += 1
    if DEBUG:
        print("n: "+str(N)+",   s: "+str(s))
    return (N/s)*bi_sum


def bfs(node, subgraph_weight, max_nodes_to_visit):

    # if max_nodes_to_visit >= W:
    #     return 0
    visited = set()
    queue = collections.deque([node])
    visited.add(node)
    n_visited = 0
    while queue:
        node = queue.popleft()
        if (node not in NEIGHBOR_DICT):
            neighbors = getNeighbors(node)
            NEIGHBOR_DICT[node] = neighbors
        else:
            neighbors = NEIGHBOR_DICT[node]

        for weight, neighbors_list in neighbors.items():
            for node_id in neighbors_list:
                if (node_id not in visited) and (weight <= subgraph_weight):
                    visited.add(node_id)
                    queue.append(node_id)

        n_visited += 1
        if n_visited >= max_nodes_to_visit:
            break
    if not queue:
        return 1
    else:
        return 0


def weightEdge(edge):
    return edge[2]


def make_set(vertice):
    parent[vertice] = vertice
    rank[vertice] = 0


def find(vertice):
    if parent[vertice] != vertice:
        parent[vertice] = find(parent[vertice])
    return parent[vertice]


def union(vertice1, vertice2):
    root1 = find(vertice1)
    root2 = find(vertice2)
    if root1 != root2:
        if rank[root1] > rank[root2]:
            parent[root2] = root1
        else:
            parent[root1] = root2
        if rank[root1] == rank[root2]:
            rank[root2] += 1


def kruskalAlgorithm():
    mst = set()
    edgeList = []
    for node in range(N):
        make_set(node)
        edges = getNeighborsKruskal(node)
        for i in edges:
            edgeList.append((node, i[0], i[1]))
    sortedEdges = sorted(edgeList, key=weightEdge)

    for edge in sortedEdges:
        v1, v2, w = edge
        # print("="*50)
        if find(v1) != find(v2):
            union(v1, v2)
            mst.add(edge)

    return deterministicWeight(mst)


def deterministicWeight(mst):
    weight = 0
    for i in mst:
        weight += i[2]
    return weight


def getNeighborsKruskal(node):
    print(node)
    sys.stdout.flush()

    if DEBUG:
        leftNeighbor = (node-1) % N
        rightNeighbor = (node+1) % N
        weight = 1
        return [(leftNeighbor, weight), (rightNeighbor, weight)]
    else:
        line = sys.stdin.readline().split()
        return [(int(line[i]), int(line[i+1])) for i in range(1, len(line), 2)]


if __name__ == '__main__':

    if DEBUG:
        N = 100  # the number of nodes
        E = 0.01  # desired accuracy (epsilon)
        W = 11  # largest weight in our graph

        def getNeighbors(node):
            leftNeighbor = (node-1) % N
            rightNeighbor = (node+1) % N
            weight1 = random.randint(1, W)
            weight2 = random.randint(1, W)
            # return [(leftNeighbor, weight1), (rightNeighbor, weight2)]
            return {weight1: [leftNeighbor], weight2: [rightNeighbor]}

    else:
        N = int(sys.stdin.readline())  # read number of nodes from the input
        # we read the desired approximation
        E = float(sys.stdin.readline()) - 1
        W = int(sys.stdin.readline())  # read the largest weight of the graph

        def getNeighbors(node):
            # ask kattis for the next node
            print(node)
            sys.stdout.flush()
            # read the answer we get from kattis
            line = sys.stdin.readline().split()
            # the answer has the form 'numNeighbors neighbor1 weight1 neighbor2 weight2 ...'
            # we want to have a list of the form:
            #[ (neighbor1, weight1), (neighbor2, weight2) , ...]

            # result = {i: () for i in range(1, W+1)}
            result = {}
            for i in range(1, len(line), 2):
                if not int(line[i+1]) in result.keys():
                    result[int(line[i+1])] = []
                result[int(line[i+1])].append(int(line[i]))
            return result
            # return [(int(line[i]), int(line[i+1])) for i in range(1, len(line), 2)]

    s1 = (int)(W*math.log(W+1)*math.log(W+1))/((E**2)*4)
    s2 = (int)(5/(E**2))
    s = min(s1, s2)
    if (W < 10):
        s = s1
    #s = min(s1, s2)
    # if W >= 10000:
    #     s = math.ceil(1.2 * (W*math.log(W+1)/(E**2)))  # choose s
    # elif W < 5:
    #     s = math.ceil((W*2)/(E**2))
    # else:
    #     s = math.ceil(6/(E**2))
    if(N > 1000):
        appr_weight = approx_mst_weight()
    else:
        appr_weight = kruskalAlgorithm()
    print("end " + str(appr_weight))
    sys.stdout.flush()
