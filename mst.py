import sys
import random
import math
import collections


DEBUG = True # False when you submit to kattis

N = 0
W = 0
E = 0.0

def approx_mst_weight():
    global N, E, W
    estimators_sum = 0
    for i in range(1, W - 1):
        estimators_sum += approx_connected_comps(i)
    return N - W + estimators_sum

def approx_connected_comps(subgraph_weight):
    global N, E, W
    s = math.ceil(10/(E^2)) # choose s
    bi_sum = 0
    for i in range(1, s):
        rand = 0.0
        while rand == 0.0:
            rand = random.uniform(1, 0)
        x = 1/rand  # choose X according to Pr[X ≥ k] = 1/k : X = 1/rand(0, 1) behaves like this : for example, P(1/rand(0,1) >= 2 ) = 1/2

        node_in_comp = False
        while not node_in_comp:
            node = random.randint(0, N-1)
            neighbors = getNeighbors(node)
            for neighbor in neighbors:
                if neighbor[1] < subgraph_weight:
                    node_in_comp = True
                    break

        bi_sum += bfs(node, neighbors, subgraph_weight, math.ceil(x))
    return (n/s)*bi_sum

def bfs(node, neighbors, subgraph_weight, max_nodes_to_visit):
    global N, E, W

    root_node = node
    visited = set()
    queue = collections.deque([node])
    visited.add(node)
    n_visited = 0
    while queue:
        node = queue.popleft()
        if node != root_node:
            neighbors = getNeighbors(node)
        for neighbor in neighbors:
            if neighbor not in visited and neighbor[1] <= subgraph_weight:
                visited.add(neighbor)
                queue.append(neighbor)
        n_visited += 1
        if n_visited == max_nodes_to_visit:
            break
    if queue.empty():
        return 1
    else:
        return 0

if __name__ == '__main__':
    global N, E, W
    if DEBUG:
        N = 6 # the number of nodes
        E = 0.1 # desired accuracy
        W = 2 # largest weight in our graph
        def getNeighbors(node):
        	leftNeighbor = (node-1) % N
        	rightNeighbor = (node+1) % N
        	weight = 1
        	return [( leftNeighbor, weight), ( rightNeighbor, weight)]
    else:
        N = int(sys.stdin.readline()) # read number of nodes from the input
    	E = float(sys.stdin.readline()) - 1 # we read the desired approximation
    	W = int(sys.stdin.readline()) # read the largest weight of the graph
        def getNeighbors(node):
        	# ask kattis for the next node
        	print(node)
        	sys.stdout.flush()
        	# read the answer we get from kattis
        	line = sys.stdin.readline().split()
        	# the answer has the form 'numNeighbors neighbor1 weight1 neighbor2 weight2 ...'
        	# we want to have a list of the form:
        	#[ (neighbor1, weight1), (neighbor2, weight2) , ...]
        	return [ (int(line[i]), int(line[i+1]) ) for i in range(1, len(line), 2)]
    appr_weight = approx_mst_weight()
    print ("end " + str(appr_weight))
    sys.stdout.flush()
