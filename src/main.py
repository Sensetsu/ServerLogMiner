import load
from collections import Counter
import math
import numpy as np

def counter_cosine_similarity(c1, c2):
    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    return dotprod / (magA * magB)

data = load.LoadLogFile()

counterA = Counter(data[0])
counterB = Counter(data[1])

print(counterA)
print(counterB)
print(counter_cosine_similarity(counterA, counterB))