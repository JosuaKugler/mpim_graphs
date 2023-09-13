import numpy as np
N = 5 #number of nodes
k = 3 #degree of nodes

# generate matrices
matrices = []
G = np.zeros((5,5))

def fill_col(col_number, matrix):
    """
    returns list with all possible matrices that differ from matrix only in this column
    """
    solutions = [matrix]
    for i in range(N-1):
        pass
    return solutions