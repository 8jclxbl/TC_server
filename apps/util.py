import numpy as np

def transpose(matrix):
    r = len(matrix)
    c = len(matrix[0])
    
    res = [[i for i in range(r)] for j in range(c)]
    for i in range(r):
        for j in range(c):
            res[j][i] = matrix[i][j]
    return res

def to_timestamp(date):
    return (date - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')