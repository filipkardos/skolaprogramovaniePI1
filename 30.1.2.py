data = [0, 4, 7, 5, 'a']

print(data)
print(f"dlzka: {len(data)}")


for i in range(0, len(data)):
    print(f"prvoknaidx:{i} je polozka: {data[i]}")  

data.append("1.AT")
data.remove(7)

for i in range(len(data)-1, 0, -1):
    print(f"prvoknaidx:{i} je polozka: {data[i]}")  







data1 = []
start1 = 0
end1= 5
step1 = 1

for i in range(start1, end1, step1):
    data1.append(i)
print(data1)

data2 = []
start2 = 5-1
end2= 0-1
step2 = -1

for i in range(start2, end2, step2):
    data2.append(i)
print(data2)

data3 = []
for i in range(1, len(data2)+1, 1):
    data3.append(data2[-i])
print(data3)