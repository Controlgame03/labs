import networkx as nx
import matplotlib.pyplot as plt
import sys


def read_adj_matrix(file_path):
    with open(file_path, 'r') as file:
        matrix = [[int(num) for num in line.split()] for line in file]
    return matrix


def isFullMatrix(matrix):
    size = len(matrix)
    for i in range(size):
        for j in range(i, size):
            if matrix[i][j] != matrix[j][i]:
                return False

    return True


def generateCombinations(n):
    if n == 0:
        return [[]]
    else:
        sub_combinations = generateCombinations(n - 1)
        result = []
        for combination in sub_combinations:
            result.append(combination + [0])
            result.append(combination + [1])
        return result


def getEdgesFromMatrix(grapMatrix):
    n = len(grapMatrix)
    edges = []
    for i in range(n):
        for j in range(n):
            if grapMatrix[i][j] == 1 and isEdgeInList(edges, (i + 1, j + 1)) == False:
                edges.append((i + 1, j + 1))

    return edges


def isEdgeInList(list, edge):
    for el in list:
        if edge[0] == el[1] and edge[1] == el[0]:
            return True

    return False


def has_path(graph, start, end, visited=None):
    if visited is None:
        visited = set()

    visited.add(start)

    if start == end:
        return True

    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            if has_path(graph, neighbor, end, visited):
                return True

    return False


if len(sys.argv) != 3:
    print("You should enter only filename and probability")
    exit()

graph = read_adj_matrix(sys.argv[1])
if isFullMatrix(graph) == False:
    print("Graph is not full")
    exit()
n = len(graph)

edges = getEdgesFromMatrix(graph)
edgeAmount = len(edges)
edgeCombinations = generateCombinations(edgeAmount)
edgeCombinationsAmount = len(edgeCombinations)

p = float(sys.argv[2])
resultProbability = 0

for i in range(edgeCombinationsAmount):
    graphDictionary = {}
    for j in range(edgeAmount):
        if edgeCombinations[i][j] == 0:
            continue
        inArray0 = False
        inArray1 = False
        for item in graphDictionary:
            if item == edges[j][0]:
                inArray0 = True
            if item == edges[j][1]:
                inArray1 = True
        if inArray0 == False:
            graphDictionary[edges[j][0]] = []
        if inArray1 == False:
            graphDictionary[edges[j][1]] = []

        graphDictionary[edges[j][0]] = graphDictionary[edges[j][0]] + [edges[j][1]]
        graphDictionary[edges[j][1]] = graphDictionary[edges[j][1]] + [edges[j][0]]
    if has_path(graphDictionary, 2, 4):
        temp = 1
        for j in range(edgeAmount):
            if edgeCombinations[i][j] == 1:
                temp = temp * p
            else:
                temp = temp * (1 - p)
        resultProbability = resultProbability + temp
        
theory = p * (p + (p ** 2) - p ** 3) * (1 + p - (p ** 2) - (p ** 3) + (p ** 4)) + (1 - p) * (p + (p ** 2) - (p ** 3) + (p ** 5) - (2 * (p ** 6)) + (p ** 7))

print("theory:   ", theory)
print("practice: ", resultProbability)

graphVisual = nx.Graph()
for i in range(len(graph)):
    for j in range(i + 1, len(graph)):
        if graph[i][j] == 1:
            # print(i + 1, j + 1)
            graphVisual.add_edge(i + 1, j + 1)

pos = nx.spring_layout(graphVisual)

node_color = 'yellow'
edge_color = 'green'
nx.draw(graphVisual, pos=pos, with_labels=True, node_color=node_color, edge_color=edge_color)
plt.axis('off')
plt.show()
