#!/usr/bin/env python3

import sys
import random
import math
import collections

DEBUG = True  # False when you submit to kattis

N = 0
W = 0
E = 0.0

NEIGHBOR_DICT = {}


def approx_mst_weight():
    # global N, E, W
    estimators_sum = 0
    i = 1
    approx_cc = 0
    while (i < W):
        # for i in range(1, W):
        approx_cc = approx_connected_comps(i)
        estimators_sum += approx_cc
        if (approx_cc < 1.5):
            estimators_sum += W-i-1
            break
        i += 1
    return N - W + estimators_sum


def approx_connected_comps(subgraph_weight):
    # global N, E, W
    s = min(math.ceil(1/(E ** 2)), N)  # choose s
    bi_sum = 0
    i = 1
    nodes_visited = [-1]
    while (i < s):
        # for i in range(1, s+1):
        rand = 0.0
        while rand == 0.0:
            rand = random.uniform(1, 0)
        # choose X according to Pr[X ≥ k] = 1/k : X = 1/rand(0, 1) behaves like this : for example, P(1/rand(0,1) >= 2 ) = 1/2
        x = 1/rand

        node_in_comp = False
        # node = random.randint(0, N-1)
        # neighbors = getNeighbors(node)

        node = -1
        while node in nodes_visited:
            node = random.randint(0, N-1)
        nodes_visited.append(node)
        # node = random.randint(0, N-1)
        # neighbors = getNeighbors(node)
        if (not node in NEIGHBOR_DICT):
            neighbors = getNeighbors(node)
        else:
            neighbors = NEIGHBOR_DICT[node]

        # for j in range(subgraph_weight, 0, -1):
        #     if not neighbors.get(j) == None:
        #         node_in_comp = True
        #         break


            # for neighbor in neighbors:
            #     if neighbor[1] <= subgraph_weight:
            #         node_in_comp = True
            #         break

        bi_sum += bfs(node, neighbors, subgraph_weight, round(x))
        i += 1
    return (N/s)*bi_sum


def bfs(node, neighbors, subgraph_weight, max_nodes_to_visit):
    # global N, E, W

    root_node = node
    visited = set()
    queue = collections.deque([node])
    visited.add(node)
    n_visited = 0
    while queue:
        node = queue.popleft()
        if node != root_node:
            if (not node in NEIGHBOR_DICT):
                neighbors = getNeighbors(node)
            else:
                neighbors = NEIGHBOR_DICT[node]


        for weight, neighbors_list in neighbors.items():
            for node_id in neighbors_list:
                if (node_id not in visited) and (weight <= subgraph_weight):
                    visited.add(node_id)
                    queue.append(node_id)
            

        # for neighbor in neighbors:
        #     if (neighbors[0] not in visited) and (neighbor[1] <= subgraph_weight):
        #         visited.add(neighbor[0])
        #         queue.append(neighbor[0])
        n_visited += 1
        if n_visited == max_nodes_to_visit:
            break
    if not queue:
        return 1
    else:
        return 0


if __name__ == '__main__':

    if DEBUG:
        N = 208  # the number of nodes
        E = 0.01  # desired accuracy (epsilon)
        W = 50  # largest weight in our graph

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

    appr_weight = approx_mst_weight()
    print("end " + str(appr_weight))
    sys.stdout.flush()
