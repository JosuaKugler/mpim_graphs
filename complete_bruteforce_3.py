import networkx as nx
from networkx.drawing.nx_pydot import write_dot
import matplotlib.pyplot as plt
import numpy as np

def get_filled_rows(max_vals, this_sum):
    """
    max_vals is a list of the maximum values that can be taken in this row
    sum is the total sum that can be achieved in this row
    """
    #find all ways to partition this_sum onto the respective row such that
    #no entry at index i is bigger than max_vals[i]
    solutions = []
    if len(max_vals) == 1:
        if this_sum <= max_vals[0]:
            return [[this_sum]]
        else:
            return []
    for i in range(min(max_vals[0], this_sum)+1):
        solutions += [[i] + solution for solution in get_filled_rows(max_vals[1:], this_sum - i)]
    return solutions

def get_filled_rows_list(previous_rows_list, N):
    previous = len(previous_rows_list)
    #maxvals is maximally 2 because we don't allow three-edges
    max_vals = [min(2, 3 - sum([previous_rows_list[i][j] for i in range(previous)])) for j in range(previous+1,N)]
    symmetric_part = [previous_rows_list[i][previous] for i in range(previous)]
    this_sum = 3 - sum(symmetric_part)
    if previous == N-2:
        actual_max_val = 3 - sum([previous_rows_list[i][N-1] for i in range(previous)])
        if this_sum == actual_max_val:
            second_to_last_row = symmetric_part + [0, this_sum]
            last_row = [previous_rows_list[i][N-1] for i in range(previous)] + [this_sum, 0]
            return [previous_rows_list + [second_to_last_row, last_row]]
        else:
            return []
    possible_next_rows = get_filled_rows(max_vals, this_sum)
    solutions = []
    for row in possible_next_rows:
        new_row = symmetric_part + [0] + row
        solutions.append(previous_rows_list + [new_row])
    return solutions #jedes Element dieser Liste ist eine Liste von Zeilen

def get_next_previous_rows_list(previous_rows_list, N):
    """
    input: a list of lists of rows
    """
    next_previous_rows_list = []
    for possible_previous_rows in previous_rows_list:
        next_previous_rows_list += get_filled_rows_list(possible_previous_rows, N)
    return next_previous_rows_list

def matrices(N):
    initial_max_vals = [2,1,1]
    for _ in range(3,N-1):
        initial_max_vals.append(0)
    print(initial_max_vals)
    previous_rows_list = [[[0] + row] for row in get_filled_rows(initial_max_vals,3)]
    for _ in range(N-2):
        previous_rows_list = get_next_previous_rows_list(previous_rows_list, N)
    return previous_rows_list

def eliminate_isomorphic_solutions(solutions):
    """
    creates a list with all graphs from solutions that are not isomorphic via is_feynman_isomorphic
    """
    new_solutions = solutions[:1]
    l =  len(solutions)
    for i, sol in enumerate(solutions[1:]):
        print(f"{i}/{l}")
        append = True
        for ref_sol in new_solutions:
            if nx.is_isomorphic(sol, ref_sol):
                append = False
        if append:
            new_solutions.append(sol)
    return new_solutions

if __name__ == "__main__":
    import pprint
    import os
    N = 8
    these_matrices = matrices(N)
    connected_graph_list = []
    for matrix in these_matrices:
        matrix = np.matrix(matrix)
        ones_matrix = np.multiply(matrix, matrix) % 3
        ones_graph = nx.from_numpy_matrix(ones_matrix)
        if nx.is_k_edge_connected(ones_graph, 2): # if graph is two connected, use matrix
            connected_graph_list.append(
                nx.from_numpy_matrix(np.matrix(matrix), parallel_edges=True, create_using = nx.MultiGraph())
                )
    
    print(len(connected_graph_list))
    graph_list = eliminate_isomorphic_solutions(connected_graph_list)
    os.system("rm test*")
    for i, G in enumerate(graph_list):
        write_dot(G, f'test{i}.dot')
        os.system(f'neato -T png test{i}.dot > test{i}.png')
