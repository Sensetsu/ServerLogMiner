import matplotlib.pyplot as plt
import numpy as np
import time
import csv
import util
import kernelDensity

#kernels = ["gaussian", "tophat", "epanechnikov"]

startTime = time.time()

logData = np.array(util.loadLogFile())
timeIntArr = util.timeStrArrToIntArr(logData[:,1])
mainDens = kernelDensity.calculate(timeIntArr, 216, "gaussian")
#testDens = kernelDensity.calculate(util.filterTimeData(timeIntArr, logData[:,3], "Wade.Carlson"), 216, "gaussian")
#kernelDensity.plot(mainDens)
#kernelDensity.plot(testDens)

densArr = []

testTime = time.time()
for timeInt in timeIntArr:
    densArr.append(kernelDensity.evaluate(timeInt, mainDens))
print("Densities evaluated in " + str((time.time() - testTime) * 1000) + " ms")

newData = np.empty((len(densArr), 11)).astype(str)

for i in range(len(densArr)):
    newData[i] = np.append(logData[i], str(densArr[i]))

with open("result.csv", "w") as file:
    writer = csv.writer(file)
    #writer.writerow(["Date","Time","Client IP","Client Name","Server IP","Server Port","Request Method","Requested Resource","Client ID","Status","Kernel Density"])
    writer.writerows(newData)

print("Operation completed in " + str((time.time() - startTime) * 1000) + " ms")