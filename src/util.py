import numpy as np
import datetime
import time

def loadLogFile():
    startTime = time.time()
    data = []

    with open("httpd.log", "r") as file:
        lines = file.read().splitlines()

        for line in lines:
            if not line:
                continue
            columns = [col.strip() for col in line.split(" ") if col]
            data.append(columns)

    print("Log file loaded in " + str((time.time() - startTime) * 1000) + " ms")
    return np.array(data)

def timeStrArrToIntArr(timeStrArr):
    startTime = time.time()
    timeIntArr = []
    for timeStr in timeStrArr:
        workingValue = time.strptime(timeStr.split(',')[0],'%H:%M:%S')
        timeIntArr.append(datetime.timedelta(hours=workingValue.tm_hour,minutes=workingValue.tm_min,seconds=workingValue.tm_sec).total_seconds())
    print("Time strings converted in " + str((time.time() - startTime) * 1000) + " ms")
    return timeIntArr

def filterTimeData(timeIntArr, conditionArr, filterValue):
    startTime = time.time()
    finalArr = []
    for i in range(len(conditionArr)):
        if (conditionArr[i] == filterValue):
            finalArr.append(timeIntArr[i])
    print("Data filtered in " + str((time.time() - startTime) * 1000) + " ms")
    return finalArr