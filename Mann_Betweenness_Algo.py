class Graph:
    def __init__(self, graph_dict={}, directed=False):
        self.graph_dict = graph_dict
        self.directed = directed

    def __str__(self):
        M = self.getMatrix()
        S = '\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in M])
        return "\n" + S + "\n"

    def nodes(self):
        return list(self.graph_dict.keys())

    def addNode(self, node_id):
        self.graph_dict[node_id] = {}
        return self

    def createEdge(self, node_idA, node_idB, weight=1):
        nodeA_connections = self.graph_dict.get(node_idA)
        nodeA_connections.update({node_idB: weight})
        self.graph_dict.update({node_idA: nodeA_connections})
        return self

    def deleteEdge(self, node_idA, node_idB):
        del self.graph_dict[node_idA][node_idB]

    def removeEdge(self, node_idA, node_idB):
        self.deleteEdge(node_idA, node_idB)
        if (not self.directed):
            self.deleteEdge(node_idB, node_idA)

    def removeNode(self, node_id):
        connections = self.graph_dict[node_id]
        for node_adj in set(connections):
            self.deleteEdge(node_id, node_adj)
            self.deleteEdge(node_adj, node_id)
        del self.graph_dict[node_id]

    def addEdge(self, node_idA, node_idB, weight=1):
        self.createEdge(node_idA, node_idB, weight)
        if (not self.directed):
            self.createEdge(node_idB, node_idA, weight)
        return self

    def getEdgeWeight(self, node_idA, node_idB):
        return self.graph_dict.get(node_idA).get(node_idB, 0)

    def getMatrix(self):
        matrix = [[self.getEdgeWeight(i, j) for j in self.nodes()] for i in self.nodes()]
        return matrix


from numpy.linalg import matrix_power


def printMatrix(M):
    S = '\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in M])
    print(S + "\n")


def Mann_betweenness(node_S, node_T, betweenness_node, matrix):
    node_S -= 1
    node_T -= 1
    betweenness_node -= 1

    fromStoT = Mann_betweenness_helper(node_S, node_T, matrix)
    printInfo(node_S, node_T, fromStoT)

    fromStoBetweenness = Mann_betweenness_helper(node_S, betweenness_node, matrix)
    printInfo(node_S, betweenness_node, fromStoBetweenness)

    fromBetweennessToT = Mann_betweenness_helper(betweenness_node, node_T, matrix)
    printInfo(betweenness_node, node_T, fromBetweennessToT)

    if fromStoBetweenness[0] + fromBetweennessToT[0] == fromStoT[0]:
        print(
            f"The number of paths from node {node_S + 1} to node {node_T + 1} through node {betweenness_node + 1} is : {fromStoBetweenness[1] * fromBetweennessToT[1]}")
    else:
        print(f"The node {betweenness_node + 1} is not the betweenness")


def Mann_betweenness_helper(node_1, node_2, matrix) -> (int, int):  # (path_len , num of paths)
    path_len = 1
    copy_matrix = matrix
    while copy_matrix[node_1][node_2] == 0:
        path_len += 1
        copy_matrix = matrix_power(matrix, path_len)
        printMatrix(copy_matrix)

    return path_len, copy_matrix[node_1][node_2]


def printInfo(node_1, node_2, fromStoT):
    print(
        f"from node ({node_1 + 1}) TO node ({node_2 + 1}) the number of shortest path is {fromStoT[1]} and the length of the path is {fromStoT[0]}")


adj_dict_weights = {
    "A": {"B": 1},
    "B": {"A": 1, "C": 1},
    "C": {"B": 1, "D": 1, "E": 1},
    "D": {"C": 1, "F": 1, "E": 1},
    "E": {"C": 1, "F": 1, "D": 1},
    "F": {"E": 1, "D": 1}
}
graph = Graph()

# Adding Nodes
for i in range(1, 7, 1):
    graph.addNode(i)
print(graph)

# "A"
graph.addEdge(1, 2)
# "B"
graph.addEdge(2, 1)
graph.addEdge(2, 3)
# "C"
graph.addEdge(3, 2)
graph.addEdge(3, 4)
graph.addEdge(3, 5)
# "D"
graph.addEdge(4, 3)
graph.addEdge(4, 5)
graph.addEdge(4, 6)
# "E"
graph.addEdge(5, 3)
graph.addEdge(5, 4)
graph.addEdge(5, 6)
# "F"
graph.addEdge(6, 4)
graph.addEdge(6, 5)

"""
# A
graph.addEdge(1, 2)
graph.addEdge(1, 3)
# B
graph.addEdge(2, 1)
graph.addEdge(2, 3)
graph.addEdge(2, 5)
# C
graph.addEdge(3, 1)
graph.addEdge(3, 2)
graph.addEdge(3, 4)
graph.addEdge(3, 5)
# D
graph.addEdge(4, 3)
# E
graph.addEdge(5, 3)
graph.addEdge(5, 2)
"""
Mann_betweenness(1, 5, 3, graph.getMatrix())
