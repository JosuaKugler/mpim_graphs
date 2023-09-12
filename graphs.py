import networkx as nx
#import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import write_dot
import networkx.algorithms.isomorphism as iso
import os

def raw_possibilities_with_one_more_loop(G):
    n = G.number_of_nodes()
    G.add_nodes_from([
        (n, {"color":"blue"}),
        (n+1, {"color":"blue"})
    ])
    solutions = []
    for edge in G.edges:
        G_new = nx.MultiGraph()
        G_new.add_nodes_from(G.nodes(data=True))
        G_new.add_edges_from(G.edges)
        G_new.add_edges_from([
            (edge[0], n),
            (n, n+1),
            (n, n+1),
            (n+1, edge[1])
        ])
        G_new.remove_edge(edge[0], edge[1])
        solutions.append(G_new)
    return solutions
    
def eliminate_isomorphic_solutions(solutions):
    """
    creates a list with all graphs from solutions that are not isomorphic via is_feynman_isomorphic
    """
    new_solutions = solutions[:1]
    for sol in solutions[1:]:
        append = True
        for ref_sol in new_solutions:
            if is_feynman_isomorpic(sol, ref_sol):
                append = False
        if append:
            new_solutions.append(sol)
    return new_solutions
    
def is_feynman_isomorpic(G1, G2):
    nm = iso.categorical_node_match("color", "blue")
    return nx.is_isomorphic(G1, G2, node_match=nm)

def add_bruteforce_loop(graphs_before):
    solutions = []
    for graph in graphs_before:
        for new_graph in raw_possibilities_with_one_more_loop(graph):
            solutions.append(new_graph)
    return eliminate_isomorphic_solutions(solutions)

if __name__ == "__main__":
    write_files = False
    if write_files:
        dirname = 'visualization'
        if not os.path.exists(dirname):
            os.mkdir(dirname)
    G0 = nx.MultiGraph()
    G0.add_nodes_from([
        (0, {"color":"red"}),
        (1, {"color":"green"})
    ])
    G0.add_edge(0,1)
    holes_dict = {0:[G0]}
    max_number_of_holes = 7
    for i in range(max_number_of_holes):
        holes_dict[i+1] = add_bruteforce_loop(holes_dict[i]) #i+1 is the new number of holes

    if write_files:
        for i in holes_dict:
            target_dir = os.path.join(dirname, f'graphs_with_{i}_holes')
            if not os.path.exists(target_dir):
                os.mkdir(target_dir)
            # write to .dot files
            for j, graph in enumerate(holes_dict[i]):
                write_dot(graph, os.path.join(target_dir, f'graph{j}.dot'))
            # compile .dot files to .pngs
            for filename in os.listdir(target_dir):
                if filename[-4:] == ".dot":
                    newfilename = filename[:-4] + '.png'
                    os.system(f'neato -T png {os.path.join(target_dir, filename)} > {os.path.join(target_dir, newfilename)}')
    else:
        for i in holes_dict:
            print(i, len(holes_dict[i]))
