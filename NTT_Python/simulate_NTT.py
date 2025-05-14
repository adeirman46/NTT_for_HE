import math

def bit_reverse(val, bits):
    reversed_val = 0
    for i in range(bits):
        if val & (1 << i):
            reversed_val |= 1 << (bits - 1 - i)
    return reversed_val

def simulate_ntt(N):
    # Langkah 1: hitung stage sebagai log2(N)
    stage = int(math.log2(N))
    print(f"Stage: {stage}")

    # Langkah 2: inisialisasi buffer dengan nilai 0
    buffer = [0] * N
    print("Initial buffer:")
    print(buffer)

    # Langkah 3: Inisialisasi inBu sebagai 2D array N/2 x N berisi 0 semua
    # inBu = [[0 for _ in range(N)] for _ in range(N // 2)]
    # print("Initial inBu[0]:")
    # print(inBu[0])  # contoh tampilan baris pertama

    # Langkah 4: inisialisasi temp dengan 0 sampai N-1
    temp = list(range(N))
    print("Initial temp:")
    print(temp)

    # Langkah 6: loop sebanyak 'stage'
    for i in range(stage):
        print(f"\n========== Stage {i+1} of {stage} ==========")

        temp = list(range(N))

        # buffer <- temp
        buffer = temp.copy()
        print("Buffer after copy from temp:")
        print(buffer)

        # clear temp
        temp = [0] * N
        print("Temp after clearing:")
        print(temp)

        m = 0
        l = 0
        half_step = 2 ** i
        full_step = 2 ** (i + 1)

        # Perbaikan: Inisialisasi inBu sesuai ukuran stage ini
        inBu = [[0 for _ in range(full_step)] for _ in range(N // full_step)]
        print("Initial inBu[0]:")
        print(inBu[0])  # contoh tampilan baris pertama

        # Salin buffer ke inBu[j][k]
        for j in range(N // full_step):
            for k in range(full_step):
                print(f"l = {l}")
                inBu[j][k] = buffer[l]
                print(f"inBu[{j}][{k}] <- buffer[{l}] = {buffer[l]}")
                l += 1

        # Proses temp menggunakan inBu
        for j in range(N // full_step):
            print(f"===== Block j = {j}")
            # === Tambahkan bit-reverse di sini ===
            bits = int(math.log2(full_step))  # jumlah bit untuk reversal
            bitrev_inBu = [0] * full_step
            for idx in range(full_step):
                rev_idx = bit_reverse(idx, bits)
                bitrev_inBu[rev_idx] = inBu[j][idx]
            inBu[j] = bitrev_inBu
            print(f"inBu[{j}] after bit-reverse: {inBu[j]}")

            for k in range(full_step):
                print(f"m = {m}")
                idx1 = k
                idx2 = idx1+1 # k + half_step
                if idx2 >= (N+1):
                    continue  # hindari out-of-bounds

                # TAMBAHKAN KODE UNTUK INI: 
                # lakukan bit reverse index inBu[j] , berikut contohnya :
                # misal, inBu[j] = [0,1,2,3,4,5,6,7] maka
                # bit reverse inBu[j] = [0,4,2,6,1,5,3,7]
                
                if m % 2 == 0:
                    print(f"temp[m] = temp[{m}] | inBu[{j}][{idx1}]= {inBu[j][idx1]} | inBu[{j}][{idx2}] = {inBu[j][idx2]} | j={j} | k={k} | k+2^{i}={idx2} | k/2={k//2}")
                else:
                    idx1 = k-1
                    idx2 = idx1+1
                    print(f"temp[m] = temp[{m}] | inBu[{j}][{idx1}]= {inBu[j][idx1]} | inBu[{j}][{idx2}] = {inBu[j][idx2]} | j={j} | k={k} | k+2^{i}={idx2} | (k-1)/2={(k-1)//2}")
                m += 1

        print("Buffer in last stage:")
        print(buffer)

        print("Temp in last stage:")
        print(temp)

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
# test_bit_reverse(8)

# Contoh pemanggilan
simulate_ntt(32)


# temp[m] = inBu[j][idx1] + inBu[j][idx2]  # <- ✅ sesuai: temp[m] <- inBu[j][k] + inBu[j][k+(2^i)]
