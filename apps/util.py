def transpose(matrix):
    r = len(matrix)
    c = len(matrix[0])
    
    res = [[i for i in range(r)] for j in range(c)]
    for i in range(r):
        for j in range(c):
            res[j][i] = matrix[i][j]
    return res