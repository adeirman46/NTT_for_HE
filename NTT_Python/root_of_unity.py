import math

def primitive_search(prime, N) :
    # Function to find all possible n-th root of unity
    possible_primitive = []
    for i in range(2,prime):
        if(pow(i,N,prime) == 1):
            possible_primitive.append(i)

    return possible_primitive

def primitive_verification(prime,N):
    # Function to verify possible n-th root of unity
    possible_primitive = primitive_search(prime,N)
    verified_primitive = []

    for scan in possible_primitive:
        existance = False
        for root_iterate in range(1,N):
            temp_pow = pow(scan,root_iterate,prime)
            existance |= (temp_pow == 1)
            if existance:
                break
    
        if not existance:
            verified_primitive.append(scan)

    return verified_primitive

def primitive_search_negative(prime,selected_primitive_positive) :
    # Function to find possible 2n-th root of unity
    possible_primitive_negative = []

    for i in range(2,prime):
        if(pow(i,2,prime)==selected_primitive_positive):
            possible_primitive_negative.append(i)

    return possible_primitive_negative


