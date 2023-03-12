import random
import sys
import matplotlib.pyplot as plt

def read_matrix(file_path='matrix.graph'):
    with open(file_path, 'r') as file:
        matrix = [[int(num) for num in line.split()] for line in file]
    return matrix

def get_eges(graph):
    graph_edges = []
    index = 0
    for i in range(0, len(graph)):
        for j in range(i + 1, len(graph[0])):
            if graph[i][j] == 1:
                graph_edges.append([i, j])
    return graph_edges

def generate_random_binary_array(size, p):
    random_array = []
    for i in range(size):
        if random.random() < float(p):
            random_array.append(1)
        else:
            random_array.append(0)
    return random_array

def print_matrix(matrix, name):
    print(name, ':')
    for i in range(len(matrix)):
        print(matrix[i])

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

def list2dict(list):
    dict = {}
    for i in range(len(list)):
        dict[list[i][0]] = []
        dict[list[i][1]] = []
    for i in range(len(list)):
        dict[list[i][0]] = dict[list[i][0]] + [list[i][1]]
        dict[list[i][1]] = dict[list[i][1]] + [list[i][0]]
    return dict

def decrease_list(list, binary_list):
    result = []
    for i in range(len(list)):
        if(binary_list[i] == 1):
            result.append(list[i])
    return result

graph = read_matrix()

print_matrix(graph, 'graph')

start_node = 2
finish_node = 4

p = []
p_size = 11
for i in range(p_size):
    p.append(0.1 * i)

epsilon = float(input('epsilon = '))

graph_edges = get_eges(graph)

n_max = round(9 / (4 * (epsilon ** 2)))
print('n_max = ', n_max)
success_sum = 0
pr = []
for p_index in range(len(p)):
    for count in range(n_max):
        binary_array = generate_random_binary_array(len(graph_edges), p[p_index])
        subgraph_edges = decrease_list(graph_edges, binary_array)
        if has_path(list2dict(subgraph_edges), start_node - 1, finish_node - 1):
            success_sum += 1

    pr.append(success_sum / n_max)
    success_sum = 0
    print('pr{', start_node, ',', finish_node, '} = ', pr[p_index], ' for p =', p[p_index])

plt.figure()
plt.title('pr{' +str (start_node) + ',' + str(finish_node) + '} (p)')
plt.plot(p, pr)
plt.show()
