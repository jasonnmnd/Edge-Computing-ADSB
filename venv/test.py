import numpy as np

randNums, tempArray = [], []
for num in range(0, 100):
    randNums.append(np.random.randint(0, 99))

randNums = np.sort(randNums)
for row in range(0, 10):
    tempArray.clear()
    for col in range(0, 10):
        tempArray.append(randNums[0])
        randNums = np.delete(randNums, 0)
    print(tempArray)
