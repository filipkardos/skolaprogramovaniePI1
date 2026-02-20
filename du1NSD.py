try:
    a = int(input("Enter a: "))
    b = int(input("Enter b: "))
except ValueError:
    print("Chyba: zadaj celé čísla")
    raise SystemExit(1)

a, b = abs(a), abs(b)
while b:
    #a, b = b, a % b
    zv = a%b
    a =b 
    b = zv
print('NSD je:', a)