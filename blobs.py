# function to generate all ordered partitions of n
f=lambda n:[x+[n-i]for i in range(n)for x in f(i)]or[[]]

#function to calcuate the number of possilbe blob-graphs from n iterations
def C(n):
    result = 0
    if n == 0 :
        result = 1
    else:    
        part_n = f(n)
        #if n==4:print("Partition_list:"+str(part_n))
        for p in part_n:

            #if n==4:print("Partition"+str(p))
            part_result = 1

            for l in p:
                k = l-1
                r =0
                if k % 2 == 0:
                    for i in range(0,int((k/2))):
                        
                        j = k-i
                        r+=C(i)*C(j)
                    C_mid = C(int(k/2))
                    part_result*=( C_mid*C_mid+C_mid)/2 +r
                if k % 2 ==1:
                    for i in range(0,int((k+1)/2)):
                        j = k-i
                        r+=C(i)*C(j) 
                    part_result *= r 
            result += part_result
    return result

