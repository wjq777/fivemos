fit =  {0: -7.654, 1: -330.9, 2: -41.36}
import time
t1 = time.clock()
b = []
for i in range(10000000):
    b.append(i*i*i*i*i)
t2 = time.clock()
print(t2-t1)

