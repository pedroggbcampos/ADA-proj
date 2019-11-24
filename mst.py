import sys
import random

DEBUG = True # False when you submit to kattis

N = 0
MAX_WEIGHT = 0
EPS = 0.0

def approx_mst_weight():
    estimators_sum = 0
    for i in range(1, W):
        estimators_sum += approx_connected_comps(i)
    return n - max_weight + estimators_sum

def approx_connected_comps(subgraph_weight):
    global n
    s = 5 # choose s                                            ???
    bi_sum = 0
    for i in range(1, s):
        x = 5 # choose X according to Pr[X ≥ k] = 1/k           ???
        bi_sum += bfs(x)
    return (n/s)*bi_sum

def bfs(max_nodes_visited):
    return 0

if __name__ == '__main__':
    global N, EPS, MAX_WEIGHT
    if DEBUG:
        N = 21000000 # the number of nodes
        EPS = 0.1 # desired accuracy
        MAX_WEIGHT = 3 # largest weight in our graph
        def getNeighbors(node):
        	leftNeighbor = (node-1) % N
        	rightNeighbor = (node+1) % N
        	weight = 1
        	return [( leftNeighbor, weight), ( rightNeighbor, weight)]
    else:
        N = int(sys.stdin.readline()) # read number of nodes from the input
    	EPS = float(sys.stdin.readline()) - 1 # we read the desired approximation
    	MAX_WEIGHT = int(sys.stdin.readline()) # read the largest weight of the graph
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
