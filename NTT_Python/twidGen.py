import math
import root_of_unity

def twiddle_generator(N, w, q):
    # 1. Calculate number of stages: stage = log2(N)
    stage = int(math.log2(N))
    
    # 2. Initialize arrW with the appropriate shape
    arrW = []
    for i in range(stage):
        arrW.append([0] * (2 ** i))  # row i has 2^i elements
    
    # 3. Fill arrW with twiddle factors
    for i in range(stage):
        k = 0
        step = (N // 2) // (2 ** i)
        for j in range(len(arrW[i])):
            arrW[i][j] = pow(w, k, q)
            k += step
        #print(f"Stage {i}: {arrW[i]}")

    # print(arrW)
    
    return arrW

# Twiddle generator
# q = 2**16+1
# N = 32
# omega = root_of_unity.primitive_verification(q,N)
# possible_negative = root_of_unity.primitive_search_negative(q,omega[0])
# psi = possible_negative[0] #psi value
# print(f"psi = {psi}")
# w = pow(psi, 2, q)
# print(f"w = {w}")
# twiddle_generator(N, w, q)