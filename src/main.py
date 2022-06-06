import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import time
import csv
import util
import kernelDensity

#kernels = ["gaussian", "tophat", "epanechnikov"]
startTime = time.time()

logData = np.array(util.loadLogFile())
mainTimeIntArr = util.timeStrArrToIntArr(logData[:,1])
mainDens = kernelDensity.calculate(mainTimeIntArr, 216, "gaussian")
cosSimDict = {}
newData = np.empty((len(logData), 11)).astype(str)

for i in range(len(logData)):
    username = logData[i,3]
    if username in cosSimDict.keys():
        newData[i] = np.append(logData[i], [str(cosSimDict[username])])
    else:
        testTimeIntArr = util.filterTimeData(mainTimeIntArr, logData[:,3], username) 
        testDens = kernelDensity.calculate(testTimeIntArr, 216, "gaussian")
        cosSimDict[username] = util.cosineSimilarity(mainDens, testDens)
        newData[i] = np.append(logData[i], [str(cosSimDict[username])])

plt.scatter(mainTimeIntArr, newData[:,10])
plt.show()

"""
dtwDict = {}
for i in range(len(logData)):
    username = logData[i,3]
    if username in dtwDict.keys():
        newData[i] = np.append(logData[i], [str(dtwDict[username])])
    else:
        testTimeIntArr = util.filterTimeData(mainTimeIntArr, logData[:,3], username) 
        testDens = kernelDensity.calculate(testTimeIntArr, 216, "gaussian")
        dtwDict[username] = dtw.calculate(mainDens, testDens, window=3)
        newData[i] = np.append(logData[i], [str(dtwDict[username])])
"""
    
with open("result.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Date","Time","Client IP","Client Name","Server IP","Server Port","Request Method","Requested Resource","Client ID","Status","Cosine Similarity"])
    writer.writerows(newData)

"""
testTimeIntArr1 = util.filterTimeData(mainTimeIntArr, logData[:,3], "Wade.Carlson")
testTimeIntArr2 = util.filterTimeData(mainTimeIntArr, logData[:,3], "Bruno.Morrow")
testTimeIntArr3 = util.filterTimeData(mainTimeIntArr, logData[:,3], "Alice.Rubio")
testDens1 = kernelDensity.calculate(testTimeIntArr1, 216, "gaussian")
testDens2 = kernelDensity.calculate(testTimeIntArr2, 216, "gaussian")
testDens3 = kernelDensity.calculate(testTimeIntArr3, 216, "gaussian")
#kernelDensity.plot(mainDens)
#kernelDensity.plot(testDens)

mainDTWMatrix = dtw.calculate(mainDens, mainDens, window=3)
print(mainDTWMatrix[len(mainDTWMatrix) - 1, len(mainDTWMatrix[0]) - 1])

testDTWMatrix1 = dtw.calculate(mainDens, testDens1, window=3)
print(testDTWMatrix1[len(testDTWMatrix1) - 1, len(testDTWMatrix1[0]) - 1])

testDTWMatrix2 = dtw.calculate(mainDens, testDens2, window=3)
print(testDTWMatrix2[len(testDTWMatrix2) - 1, len(testDTWMatrix2[0]) - 1])

testDTWMatrix3 = dtw.calculate(mainDens, testDens3, window=3)
print(testDTWMatrix3[len(testDTWMatrix3) - 1, len(testDTWMatrix3[0]) - 1])
"""

"""
mainDensArr = []
testDensArr = []

testTime = time.time()
for timeInt in mainTimeIntArr:
    mainDensArr.append(kernelDensity.evaluate(timeInt, mainDens))

for timeInt in testTimeIntArr:
    testDensArr.append(kernelDensity.evaluate(timeInt, testDens))
print("Densities evaluated in " + str((time.time() - testTime) * 1000) + " ms")

meanDens = np.mean(mainDensArr)
medianDens = np.median(mainDensArr)
print("Mean density: " + str(meanDens))
print("Median density: " + str(medianDens))

testTime = time.time()
zScoreArr = stats.zscore(testDensArr)
print("Z Scores calculated in " + str((time.time() - testTime) * 1000) + " ms")

plt.scatter(mainTimeIntArr, mainDensArr, s=0.5)
plt.scatter(testTimeIntArr, testDensArr, s=0.5)
plt.show()
"""

"""
newData = np.empty((len(mainDensArr), 13)).astype(str)

for i in range(len(densArr)):
    newData[i] = np.append(logData[i], [str(timeIntArr[i]), str(densArr[i]), str(zScoreArr[i])])

with open("result.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Date","Time","Client IP","Client Name","Server IP","Server Port","Request Method","Requested Resource","Client ID","Status","Time Int","Kernel Density","Z Score"])
    writer.writerows(newData)
"""
print("Operation completed in " + str((time.time() - startTime) * 1000) + " ms")