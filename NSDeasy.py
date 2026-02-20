a = int(input("Enter a: "))
b = int(input("Enter b: "))

while b:
    zv = a%b
    a =b 
    b = zv
    
print('NSD je:', a)