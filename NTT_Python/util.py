import numpy as np
import math

def reverse(n,width): #reversing bits for matrix index
    new_n = 0
    for i in range(width):
        new_n <<= 1
        if n & 1:
            new_n ^= 1
        n >>= 1
    return new_n

def bit_reverse(buffer,N): #reversing the buffer 
    width = int(math.log2(N))
    buffer_temp = []
    for scan in range(0,len(buffer)):
        buffer_temp.append(buffer[reverse(scan,width)])
    return buffer_temp
    


def base_NTT(A,N,q,psi):
    B = [0] * N
    for j in range(0,N):
        for i in range(0,N):
            temp = B[j]
            B[j] = temp + (A[i] * pow(psi, 2*i*j+i,q))%q
        B[j] = B[j]%q
    #print(f'NTT Base Equation: {B}')
    return B

def p2p_mult(A,B,q):
    C = [0]*len(A)
    for scan in range (0,len(A)):
        C[scan] = (A[scan]*B[scan])%q
    return C

def benchmark(A,B,N,q):
    A = np.flip(A)
    B = np.flip(B)



    C =  np.polymul(A,B)
    D = [0]*(N+1)
    D[0] = 1
    D[N]=1
    E = np.polydiv(C,D)
    for scan in range(0,len(E[1])):
        E[1][scan]= (E[1][scan])%q
    
    return E[1]

def scaling_factor(A,n_inv,q):
    for scan in range(0,len(A)):
        A[scan]= (A[scan]*n_inv)%q

     