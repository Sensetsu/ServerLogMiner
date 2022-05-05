import numpy as np
import datetime

def LoadLogFile():
    startTime = datetime.datetime.now()
    data = []

    with open("httpd.log", "r") as file:
        lines = file.read().splitlines()

        for line in lines:
            if not line:
                continue
            columns = [col.strip() for col in line.split(" ") if col]
            data.append(columns)

    print("Loaded in " + str((datetime.datetime.now() - startTime).microseconds / 1000) + " ms")
    return np.array(data)