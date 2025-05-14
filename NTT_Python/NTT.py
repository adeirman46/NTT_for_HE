import math

def bit_reverse(val, bits):
    reversed_val = 0
    for i in range(bits):
        if val & (1 << i):
            reversed_val |= 1 << (bits - 1 - i)
    return reversed_val

def bit_reverse_array(arr):
    N = len(arr)
    bits = int(math.log2(N))
    result = [0] * N
    for i in range(N):
        rev_i = bit_reverse(i, bits)
        result[rev_i] = arr[i]
    return result


def ntt(N, arrW, q, arrPol): 
    print("======== START NTT ========")
    #print("Original Polynomial:")
    #print(arrPol)

    # Bit reversal on input
    a = bit_reverse_array(arrPol)
    #print("\nAfter Bit-Reversal Permutation:")
    #print(a)

    stage_count = int(math.log2(N))
    #print(f"\nTotal stages: {stage_count}")

    for stage in range(stage_count):
        m = 2 ** (stage + 1)
        half_m = m // 2
        #print(f"\n--- Stage {stage+1}/{stage_count} ---")
        #print(f"Butterfly size: {m}, Half size: {half_m}")
        #print(f"Twiddle factors: {arrW[stage]}")

        for k in range(0, N, m):
            for j in range(half_m):
                u = a[k + j]
                t = a[k + j + half_m] * arrW[stage][j] % q
                a[k + j] = (u + t) % q
                a[k + j + half_m] = (u - t + q) % q
                #print(f"  [k={k}, j={j}] u={u}, t={t}, w={arrW[stage][j]}")
                #print(f"    -> a[{k + j}] = {a[k + j]}, a[{k + j + half_m}] = {a[k + j + half_m]}")

    print("\nNTT Output:")
    print(a)
    return a

def intt(N, arrW_inv, q, arrPolNtt, N_inv): 
    print("======== START INTT ========")
    #print("Input from NTT:")
    #print(arrPolNtt)

    # Bit reversal on input
    # a = bit_reverse_array(arrPolNtt)
    # print("\nAfter Bit-Reversal Permutation:")
    a = arrPolNtt
    #print(a)

    stage_count = int(math.log2(N))
    #print(f"\nTotal stages: {stage_count}")

    for stage in range(stage_count):
        m = 2 ** (stage + 1)
        half_m = m // 2
        #print(f"\n--- Stage {stage+1}/{stage_count} ---")
        #print(f"Butterfly size: {m}, Half size: {half_m}")
        #print(f"Twiddle factors (inverse): {arrW_inv[stage]}")

        for k in range(0, N, m):
            for j in range(half_m):
                u = a[k + j]
                v = a[k + j + half_m]
                t = v * arrW_inv[stage][j] % q
                a[k + j] = (u + t) % q
                a[k + j + half_m] = (u - t + q) % q
                #print(f"  [k={k}, j={j}] u={u}, v={v}, w_inv={arrW_inv[stage][j]}, t={t}")
                #print(f"    -> a[{k + j}] = {a[k + j]}, a[{k + j + half_m}] = {a[k + j + half_m]}")

    # Final normalization (multiply each element by N_inv mod q)
    #print(f"\nApplying N_inv = {N_inv}")
    for i in range(N):
        a[i] = a[i] * N_inv % q
        #print(f"a[{i}] * N_inv = {a[i]}")

    print("\nINTT Output:")
    print(a)
    return a


def test_bit_reverse(N):
    bits = int(math.log2(N))
    original = list(range(N))
    bitrev_result = [0] * N

    for i in range(N):
        rev_i = bit_reverse(i, bits)
        bitrev_result[rev_i] = original[i]
        print(f"Index {i:0{bits}b} (dec {i}) -> Bit-reversed: {rev_i:0{bits}b} (dec {rev_i})")

    print("\nOriginal indices:")
    print(original)
    print("Bit-reversed indices:")
    print(bitrev_result)


# Contoh pemanggilan
# ntt(32)


