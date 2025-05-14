import math
# import Radix_2
# import Radix_4
# import Radix_8
import util
import root_of_unity
import time
start_time = time.time()
run_time = time.time()
def testing(loop:bool, max_exp:int):
    q = 2**16+1
    if loop:
        for i in range(1,max_exp+1):
            print('----------------------')
            global start_time
            start_time = time.time()
            N = 2**i

            #GENERATING PRIMITIVES AND OTHER METRICS
            omega = root_of_unity.primitive_verification(q,N)
            possible_negative = root_of_unity.primitive_search_negative(q,omega[0])
            psi = possible_negative[0] #psi value
            print(f'[INFO] Finding root of unity finished {round(time.time()-start_time,4)} seconds after starting {N} point')
            n_inv = pow(N,-1,q) #inverse of N
            w_4th = pow(psi,N//2,q) #w_4th for radix 4 (NTT)
            w_4th_inv = pow(w_4th,-1,q) #inverse of w_4th for radix 4 (INTT)
            w_8th = pow(psi,N//4,q) #w_8th for radix 8 (NTT)
            w_8th_inv = pow(w_8th,-1,q) #inverse of w_8th for radix 8 (INTT)

            A = [i for i in range(N)]

            # NTT Calculation
            in_NTT = util.bit_reverse(A,N)
            ntt = scheduling_NTT(in_NTT.copy(), N, q, psi, w_8th, w_4th)
            print(f'[INFO] Combine Radix NTT calculation finished {round(time.time()-start_time,4)} seconds after starting {N} point')
            # Bse NTT Calculation
            base = util.base_NTT(A.copy(),N,q,psi)
            print(f'[INFO] Base NTT calculation finished {round(time.time()-start_time,4)} seconds after starting {N} point')

            match_ntt = ntt==base
            if not match_ntt:
                print(f'[ERROR] NTT Does NOT match for {N} point') 
                break
            else: print(f'[INFO] NTT Match Uniquely for {N} point.\n[INFO] Finished {round(time.time()-start_time,4)} seconds after starting {N} point')

            # INTT Calculation
            intt = scheduling_INTT(ntt.copy(),N, q, psi, w_8th_inv, w_4th_inv)
            util.scaling_factor(intt,n_inv,q)
            intt = util.bit_reverse(intt,N)
            print(f'[INFO] Combine Radix INTT calculation finished {round(time.time()-start_time,4)} seconds after starting {N} point')

            match_intt = intt==A
            if not match_intt:
                print(f'[ERROR] INTT Does NOT match for {N} point') 
                break
            else: print(f'[INFO] INTT Match Uniquely for {N} point.\n[INFO] Finished {round(time.time()-start_time,4)} seconds after starting {N} point')
        if match_ntt & match_intt: print(f'[INFO] NTT and INTT Match Uniquely until {2**(max_exp)} point')

    else: #NOT LOOPING
        N = 2**max_exp 

        #GENERATING PRIMITIVES AND OTHER METRICS
        omega = root_of_unity.primitive_verification(q,N)
        possible_negative = root_of_unity.primitive_search_negative(q,omega[0])
        psi = possible_negative[0] #psi value
        print(f'[INFO] Finding root of unity finished {round(time.time()-start_time,4)} seconds after starting {N} point')
        n_inv = pow(N,-1,q) #inverse of N
        w_4th = pow(psi,N//2,q) #w_4th for radix 4 (NTT)
        w_4th_inv = pow(w_4th,-1,q) #inverse of w_4th for radix 4 (INTT)
        w_8th = pow(psi,N//4,q) #w_8th for radix 8 (NTT)
        w_8th_inv = pow(w_8th,-1,q) #inverse of w_8th for radix 8 (INTT)

        A = [i for i in range(N)]
        print(f"A before bit reverse : {A}\n")

        # NTT Calculation
        in_NTT = util.bit_reverse(A,N)
        print(f"A after bit reverse : {in_NTT}\n")
        ntt = scheduling_NTT(in_NTT.copy(), N, q, psi, w_8th, w_4th)
        print(f'[INFO] Combine Radix NTT calculation finished {round(time.time()-start_time,4)} seconds after starting {N} point')
        # Bse NTT Calculation
        base = util.base_NTT(A.copy(),N,q,psi)
        print(f'[INFO] Base NTT calculation finished {round(time.time()-start_time,4)} seconds after starting {N} point')

        match = ntt==base
        if not match: print(f'[ERROR] NTT Does NOT match for {N} point')
        else: print(f'[INFO] NTT Match Uniquely for {2**(max_exp)} point')

        # INTT Calculation
        intt = scheduling_INTT(ntt.copy(),N, q, psi, w_8th_inv, w_4th_inv)
        util.scaling_factor(intt,n_inv,q)
        intt = util.bit_reverse(intt,N)
        print(f'[INFO] Combine Radix INTT calculation finished {round(time.time()-start_time,4)} seconds after starting {N} point')

        match = intt == A
        if not match: print(f'[ERROR] INTT Does NOT match for {N} point')
        else: print(f'[INFO] INTT Match Uniquely for {2**(max_exp)} point')

#SCHEDULER
def staging(point,N,radix_usage):
    if (point == 1):
        print("done")
    else:
        exp = int(math.log(N,2))
        radix_usage[0] = exp//3; exp -= radix_usage[0]*3
        radix_usage[1] = exp//2; exp -= radix_usage[1]*2
        radix_usage[2] = exp//1

        # if (math.log2(point)%3==0):
        #     point = point/8
        #     #A = Radix_8.Radix_8_NTT(A, N, q, psi, w_8th,stage)
        #     radix_usage[0] = radix_usage[0]+1
        #     staging(point,A, N, q, psi, w_8th, w_4th,stage,radix_usage)

            
        # elif (math.log2(point)%2==0):
        #     point = point/4
        #     #A = Radix_4.Radix_4_NTT(A, N, q, psi, w_4th,stage)
        #     radix_usage[1] = radix_usage[1]+1
        #     staging(point,A, N, q, psi, w_8th, w_4th,stage,radix_usage)
           
        # else:
        #     point = point/2
        #     #A = Radix_2.Radix_2_NTT(A, N, q, psi,stage)
        #     radix_usage[2] = radix_usage[2]+1
        #     staging(point,A, N, q, psi, w_8th, w_4th,stage,radix_usage)


def scheduling_NTT(A, N, q, psi, w_8th, w_4th):
    print(f'[INFO] Calculating NTT')
    radix_usage =[0,0,0] #number of times the radix is called (starting from radix 8 to 2)
    staging(N,N,radix_usage)
    print(f'Radix Usage: {radix_usage}')
    global start_time
    for stage in range(0,radix_usage[0]):
        A = Radix_8.Radix_8_NTT(A, N, q, psi, w_8th,stage)
        print(f"radix 8 : {stage} --- {round(time.time()-start_time,4)} seconds")
    for stage in range(radix_usage[0], radix_usage[1]+radix_usage[0]):
        A = Radix_4.Radix_4_NTT(A, N, q, psi, w_4th,stage*1.5)
        print(f"radix 4 : {stage} --- {round(time.time()-start_time,4)} seconds")
    for stage in range(radix_usage[0]*3+radix_usage[1]*2,radix_usage[2]+radix_usage[0]*3+radix_usage[1]*2):
        A = Radix_2.Radix_2_NTT(A, N, q, psi,stage)
        print(f"radix 2 : {stage} --- {round(time.time()-start_time,4)} seconds")

    return A

def scheduling_INTT(A, N, q, psi, w_8th_inv, w_4th_inv):
    print(f'[INFO] Calculating INTT')
    radix_usage =[0,0,0] #number of times the radix is called (starting from radix 8 to 2)
    staging(N,N,radix_usage)
    print(f'Radix Usage: {radix_usage}')
    global start_time
    temp = N

    for stage in range(radix_usage[0]):
        temp = temp//8
        A = Radix_8.Radix_8_INTT(A, N, q, psi, w_8th_inv,temp)
        print(f"radix 8 : {stage} --- {round(time.time()-start_time,4)} seconds")
    for stage in range(radix_usage[1]):
        temp = temp//4
        A = Radix_4.Radix_4_INTT(A, N, q, psi, w_4th_inv,temp)
        print(f"radix 4 : {stage} --- {round(time.time()-start_time,4)} seconds")
    for stage in range(radix_usage[2]-1,-1,-1):
        A = Radix_2.Radix_2_INTT(A, N, q, psi,stage)
        print(f"radix 2 : {stage} --- {round(time.time()-start_time,4)} seconds")

    return A

#TESTING GROUND

testing(loop=False,max_exp=3)
# testing(loop=False,max_exp=10)
print('-----------')
print(f'Program finished running for {round(time.time()-run_time,4)} seconds')