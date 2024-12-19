import numpy as np

def strassen_multiply(A, B):
    n = len(A)
    if n == 1:
        return A * B
    else:
        mid = n // 2
        
        A11 = A[:mid, :mid]
        A12 = A[:mid, mid:]
        A21 = A[mid:, :mid]
        A22 = A[mid:, mid:]
        
        B11 = B[:mid, :mid]
        B12 = B[:mid, mid:]
        B21 = B[mid:, :mid]
        B22 = B[mid:, mid:]

        # Calculando as 7 multiplicações de Strassen
        M1 = strassen_multiply(A11 + A22, B11 + B22)
        M2 = strassen_multiply(A21 + A22, B11)
        M3 = strassen_multiply(A11, B12 - B22)
        M4 = strassen_multiply(A22, B21 - B11)
        M5 = strassen_multiply(A11 + A12, B22)
        M6 = strassen_multiply(A21 - A11, B11 + B12)
        M7 = strassen_multiply(A12 - A22, B21 + B22)

        # Combinando os resultados em uma única matriz
        C11 = M1 + M4 - M5 + M7
        C12 = M3 + M5
        C21 = M2 + M4
        C22 = M1 - M2 + M3 + M6

        C = np.vstack((np.hstack((C11, C12)), np.hstack((C21, C22))))
        return C

def square_matrix_multiply_recursive(A, B):
    n = A.shape[0]
    C = np.zeros((n, n))
    
    if n == 1:
        C[0, 0] = A[0, 0] * B[0, 0]
    else:
        # Divide as matrizes A e B em submatrizes de tamanho n/2
        mid = n // 2
        A11, A12, A21, A22 = A[:mid, :mid], A[:mid, mid:], A[mid:, :mid], A[mid:, mid:]
        B11, B12, B21, B22 = B[:mid, :mid], B[:mid, mid:], B[mid:, :mid], B[mid:, mid:]
        
        # Calcula cada quadrante da matriz C
        C[:mid, :mid] = square_matrix_multiply_recursive(A11, B11) + square_matrix_multiply_recursive(A12, B21)
        C[:mid, mid:] = square_matrix_multiply_recursive(A11, B12) + square_matrix_multiply_recursive(A12, B22)
        C[mid:, :mid] = square_matrix_multiply_recursive(A21, B11) + square_matrix_multiply_recursive(A22, B21)
        C[mid:, mid:] = square_matrix_multiply_recursive(A21, B12) + square_matrix_multiply_recursive(A22, B22)
    
    return C

def multiply_matrices_basic(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            C[i][j] = 0
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C
