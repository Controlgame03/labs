import math
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

def generate_random_binary_array(size, p, weight=None):
    random_array = []
    if(weight == None):
        for i in range(size):
            if random.random() < float(p):
                random_array.append(1)
            else:
                random_array.append(0)
    elif weight == 0 or p == 0:
        for i in range(size):
            random_array.append(0)
    elif p == 1:
        for i in range(size):
            random_array.append(1)
    else:
        for i in range(size):
            random_array.append(0)
        while get_weight(random_array) != weight:

            rand_index = random.randint(0, len(random_array) - 1)
            random_array[rand_index] = (random_array[rand_index] + 1) % 2
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

def get_weight(array):
    result = 0
    for i in range(len(array)):
        if(array[i] != 0):
            result += 1
    return result

def stratify_n_max(n_max, parts):
    n_j = [0]
    for i in range(parts):
        n_j.append(int(n_max / parts))
    n_j[len(n_j) - 1] += (n_max - sum(n_j))
    return n_j

def factorial(num):
    f = 1
    for i in range(2, num + 1):
        f *= i
    return f


def combinations(k, n):
    return factorial(n) / (factorial(k) * factorial(n - k))

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
l = len(graph_edges)
n_for_weight = stratify_n_max(n_max, l)


probability = [0]
for p_index in range(1, len(p)):

    probability_for_weight = [0]
    success_sum = 0
    for current_weight in range(1, len(n_for_weight)):
        for count in range(n_for_weight[current_weight]):
            binary_array = generate_random_binary_array(len(graph_edges), p[p_index], current_weight)
            subgraph_edges = decrease_list(graph_edges, binary_array)
            if has_path(list2dict(subgraph_edges), start_node - 1, finish_node - 1):
                success_sum += 1
        probability_for_weight.append(success_sum / n_for_weight[current_weight])
        success_sum = 0

    result_sum = 0
    for current_weight in range(1, len(probability_for_weight)):
        comb = combinations(current_weight, l)
        current_weight_probability = combinations(current_weight, l) * (p[p_index] ** current_weight) * ((1 - p[p_index]) ** (l - current_weight))
        result_sum += current_weight_probability * probability_for_weight[current_weight]
    probability.append(result_sum)


for i in range(len(probability)):
    print('pr{', start_node, ',', finish_node, '} = ', probability[i], ' for p =', 0.1 * i)

plt.figure()
plt.title('pr{' + str (start_node) + ',' + str(finish_node) + '} (p)')
plt.plot(p, probability)
plt.show()
