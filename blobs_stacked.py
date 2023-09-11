def C(n):
    result = 0
    if n == 1 or n ==2 or n ==0:
        return 1
    else:
        k = n-1
        if k % 2 == 0:
            for i in range(0,int((k/2))):
                j = k-i
                result+=C(i)*C(j)
            result+= (C(k/2)*C(k/2)+C(k/2))/2
        if k % 2 ==1:
            for i in range(0,int((k+1)/2)):
                j = k-i
                result+=C(i)*C(j)
        return result
for n in range(1,100):
    print(str(n)+":")
    print(C(n))
