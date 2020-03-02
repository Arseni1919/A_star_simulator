import math
import numpy as np
# heuristic_func = lambda a,b: 0
# print(heuristic_func('vfvf',2))

# print(np.random.choice(5, 5, replace=False, p=[0.01, 0.01, 0.01, 0.01, 0.96]))
# print(np.random.choice(5, 5, replace=True, p=[0.01, 0.01, 0.01, 0.01, 0.96]))
# print(np.random.choice(5, 5, p=[0.01, 0.01, 0.01, 0.01, 0.96]))

print(np.mean([1,2,3,4]))
import os.path

if os.path.isfile('building-1/map-1-ATB.piv'):
    print("File exist")
else:
    print("File not exist")
