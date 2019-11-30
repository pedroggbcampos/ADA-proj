#!/usr/bin/env python3

import sys
import random

DEBUG = True # False when you submit to kattis

# function which queries the next set of neighbors from kattis
if DEBUG:
	N = 21000000 # the number of nodes
	eps = 0.1 # desired accuracy
	maxWeight = 3 # largest weight in our graph
	# we will simulate a graph that is just one large cycle
	# you could add some other types of graphs for debugging/testing your program
	def getNeighbors(node):
		leftNeighbor = (node-1) % N
		rightNeighbor = (node+1) % N
		weight = 1
		return [( leftNeighbor, weight), ( rightNeighbor, weight)]
else:
	N = int(sys.stdin.readline()) # read number of nodes from the input
	eps = float(sys.stdin.readline()) - 1 # we read the desired approximation
	maxWeight = int(sys.stdin.readline()) # read the largest weight of the graph
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

		
# Now we try to estimate the size of a minimum spanning forest.
# Note that the example below is completely wrong and will not give a correct result!
# The example is just here to show how to use the function 'getNeighbors'

# We now compute the average edge weight of 100 random neighborhoods
sumOfWeights = 0
numEdges = 0
for i in range(1, 100):
	node = random.randint(0, N-1) # sample a random node
	neighbors = getNeighbors(node) # get the list of neighbors and the corresponding weights
	for neighbor, weight in neighbors:
		sumOfWeights += weight
		numEdges += 1
averageEdgeWeight = 1.0 * sumOfWeights / numEdges
# A spanning tree always consists of N-1 edges,
# so one could think a minimum spanning tree would have roughly the following weight.
# (Note: This idea is wrong because a MINIMUM spanning tree will try to use only small edges)
weightOfSpanningTree = averageEdgeWeight * (N-1)

# print the answer
print('end ' + str(weightOfSpanningTree))
sys.stdout.flush()
