n = int(input("enter n:"))

#for i in range(1, n+1):
#    f = f*i
#    print(f)


value = 5
def qwer(n):
    if(n == 1):
        return 1
    return n*qwer(n-1)

print(qwer(value))