#!/usr/bin/env python3

import sys
import random
import math
import collections
# import numpy

# False when you submit to kattis
# DEBUG = True
DEBUG = False

N = 0
W = 0
E = 0.0

NEIGHBOR_DICT = {}


def approx_mst_weight():

    estimators_sum = 0
    i = 1
    approx_cc = 0
    while (i < W):
        approx_cc = approx_connected_comps(i)
        estimators_sum += approx_cc
        # if (approx_cc < 1.5):
        #     # estimators_sum += W-i-1
        #     break
        i += 1
    last_acc = approx_connected_comps(W)
    if (last_acc > 5):
        estimators_sum += (last_acc + 1)
        estimators_sum -= (approx_cc-1)*(W+1)
    return N - W + estimators_sum


def approx_connected_comps(subgraph_weight):
    s = min(math.ceil(4/(E**2)), N)  # choose s
    # s = N/100
    # s = math.ceil(5/(E**2))  # choose s
    bi_sum = 0
    i = 1
    # nodes_visited = [-1]
    while (i < s):
        # rand = numpy.random.random_sample()
        # rand = random.random()
        # choose X according to Pr[X ≥ k] = 1/k : X = 1/rand(0, 1) behaves like this : for example, P(1/rand(0,1) >= 2 ) = 1/2
        x = 1/random.uniform(0, 1)

        # node_in_comp = False

        # node = -1
        # while node in nodes_visited:
        node = random.randint(0, N-1)
        # nodes_visited.append(node)

        bi_sum += bfs(node, subgraph_weight, math.floor(x))
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


if __name__ == '__main__':

    if DEBUG:
        N = 4_000  # the number of nodes
        E = 0.01  # desired accuracy (epsilon)
        W = 10  # largest weight in our graph

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
