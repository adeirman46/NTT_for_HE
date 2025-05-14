import root_of_unity
import twidGen
import NTT
import time 
import numpy as np

def generate_polynomial_array(N):
    arrPol = list(range(N))  # Membuat array dengan elemen 0 sampai N-1
    return arrPol

def check_array(array1, array2, tolerance=1e-6):
    """
    Membandingkan dua array (integer atau float) berdimensi sama.
    Untuk float, digunakan toleransi perbandingan.
    
    Parameters:
    - array1, array2: list atau numpy array dengan dimensi sama
    - tolerance: toleransi untuk float comparison (default: 1e-6)
    
    Returns:
    - True jika sama (atau dalam toleransi), False jika tidak
    """
    array1 = np.array(array1)
    array2 = np.array(array2)

    if array1.shape != array2.shape:
        print("Dimensi array tidak sama.")
        return False

    # Jika array bertipe float, gunakan toleransi
    if np.issubdtype(array1.dtype, np.floating) or np.issubdtype(array2.dtype, np.floating):
        if np.allclose(array1, array2, atol=tolerance):
            print("Isi array sudah sama (dalam toleransi).")
            return True
        else:
            print("Isi array belum sama (float, dengan toleransi).")
            beda = np.where(np.abs(array1 - array2) > tolerance)
    else:
        # Untuk integer, perbandingan langsung
        if np.array_equal(array1, array2):
            print("Isi array sama persis (integer).")
            return True
        else:
            print("Isi array belum sama (integer).")
            beda = np.where(array1 != array2)

    print("Perbedaan ditemukan pada indeks:", beda)
    print("Nilai array1:", array1[beda])
    print("Nilai array2:", array2[beda])
    return False

def main(q,N):
    # Mulai hitung waktu
    start_time = time.time()

    # Generate primitive
    omega = root_of_unity.primitive_verification(q, N)
    possible_negative = root_of_unity.primitive_search_negative(q, omega[0])
    psi = possible_negative[0]  # psi value
    # print(f"psi = {psi}")

    # Generate omega for NTT
    w = pow(psi, N, q)
    # print(f"w = {w}")

    # Simpan hasil twiddle factors ke arrW
    arrW = twidGen.twiddle_generator(N, w, q)

    # Generate N-degree polynomial
    arrPol = generate_polynomial_array(N)
    print("Array input NTT:")
    print(arrPol)

    # Waktu mulai NTT
    start_ntt_time = time.time()

    # # Calculate NTT
    mode = 0 
    print("\n==================Start NTT:==================")
    arrPolNtt = NTT.ntt(N, arrW, q, arrPol)

    # Waktu selesai NTT
    end_ntt_time = time.time()

    # # Generate omega for INTT
    print("\n==================Metrics for INTT:==================")
    N_inv = pow(N, -1, q)
    w_inv = pow(psi, -1*N, q) 
    # print(f"w_inv = {w_inv}")      

    # # Simpan hasil twiddle factors ke arrW_inv
    arrW_inv = twidGen.twiddle_generator(N, w_inv, q)
    # print(arrW_inv)

    # Perform bit-reversal on the NTT result before INTT
    arrPolNtt_reversed = NTT.bit_reverse_array(arrPolNtt)
    # print("arrPolNtt after reversed bit:")
    # print(arrPolNtt_reversed)

    # Waktu mulai INTT
    start_intt_time = time.time()

    # # Calculate INTT
    mode = 1 
    print("\n==================Start INTT:==================")
    arrPolIntt = NTT.intt(N, arrW_inv, q, arrPolNtt_reversed, N_inv)

    # Waktu selesai NTT
    end_intt_time = time.time()

    print(f"\nWaktu generate primitive dan twiddle factor = {-(start_time-start_ntt_time)} sekon")
    print(f"Waktu eksekusi NTT = {-(start_ntt_time-end_ntt_time)} sekon")
    print(f"Waktu eksekusi INTT = {-(start_intt_time-end_intt_time)} sekon")
    print(f"Waktu eksekusi NTT-INTT = {-(start_ntt_time-end_intt_time)} sekon")
    print(f"Waktu eksekusi dari generate primitiv hingga akhir NTT = {-(start_time-end_ntt_time)} sekon")
    print(f"Waktu eksekusi dari generate primitiv hingga akhir INTT = {-(start_time-end_intt_time)} sekon")

    return arrPol, arrPolIntt

if __name__ == "__main__": 
    q = 7681#2**16+1
    N = 4#4096
    arrPol, arrPolIntt = main(q, N)
    check_array(arrPol, arrPolIntt)

    # cache = NTT.bit_reverse_array([0, 7, 1, 6, 2, 5, 3, 4])
    # print(cache)

    # arrPolNtt = NTT.ntt_intt(N, arrW, q, arrPol, mode=0, N_inv=N_inv)
    # arrPolIntt = NTT.ntt_intt(N, arrW_inv, q, arrPolNtt, mode=1, N_inv=N_inv)

    # print("Input awal :", arrPol)
    # print("Setelah NTT:", arrPolNtt)
    # print("Setelah INTT:", arrPolIntt) [0, 6, 4, 2, 1, 7, 5, 3] [0, 5, 7, 2, 1, 4, 6, 3]