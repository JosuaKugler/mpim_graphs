# function to generate all ordered partitions of n
f=lambda n: [x+[n-i] for i in range(n) for x in f(i)] or [[]]

#function to calcuate the number of possilbe blob-graphs from n iterations
def C(n):
    n = int(n)
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

def C_two_connected(n):
    if n == 1:
        return 1
    result = 0
    if (n-1)%2 == 0:
        for i in range(int(n/2)): 
            j = n-1 - i
            assert( i < j )
            result += C(i) * C(j)
        result += (C((n-1)/2)**2 + C((n-1)/2))/2
    else:
        for i in range(int(n/2)):
            j = n-1 - i
            assert( i < j )
            result += C(i) * C(j)
    return result

three_partition = lambda n : [[a,b,n-(a+b)] for a in range(n+1) for b in range(n+1 - a)]

vertex_correction_labelled_values = {0:1}

def vertex_correction_labelled(n):
    """
    compute the number of possible graphs for n holes where three outer labelled vertices are given
    """
    try:
        result = vertex_correction_labelled_values[n]
    except:
        result = 0
        for partition in three_partition(n-1):
            a,b,c = partition
            result += vertex_correction_labelled(a) * vertex_correction_labelled(b) * vertex_correction_labelled(c)
        vertex_correction_labelled_values[n] = result
    return result

if __name__ == "__main__":
    import sys
    import math
    try:
        n = int(sys.argv[1])
    except:
        n = 1
    #for i in range(n):
    #    print(int(C_two_connected(i)))
    import matplotlib.pyplot as plt
    xs = range(n)
    ys = []
    for x in xs:
        ys.append(math.log(vertex_correction_labelled(x)))
    plt.plot(xs, ys)
    #print(vertex_correction_labelled_values)
    plt.show()
