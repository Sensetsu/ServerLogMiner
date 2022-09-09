# Author: Jake Vanderplas <jakevdp@cs.washington.edu>
#
import time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity
from sklearn.utils.fixes import parse_version

# `normed` is being deprecated in favor of `density` in histograms
if parse_version(matplotlib.__version__) >= parse_version("2.1"):
    density_param = {"density": True}
else:
    density_param = {"normed": True}


def calculate(timeIntArr, max_value, numSamples, kernel, bandwidth=0.5):
    startTime = time.time()
    X = np.array(timeIntArr).reshape(-1, 1)

    X_plot = np.linspace(0, max_value, numSamples)[:, np.newaxis]

    kde = KernelDensity(kernel=kernel, bandwidth=bandwidth).fit(X)
    densityArr = np.exp(kde.score_samples(X_plot))
    print("Kernel density calculated in " + str((time.time() - startTime) * 1000) + " ms")
    return densityArr

def plot(densityArr, max_value):
    startTime = time.time()
    X_plot = np.linspace(0, max_value, len(densityArr))[:, np.newaxis]
    fig, ax = plt.subplots()
    lw = 2
    ax.plot(
        X_plot[:, 0],
        densityArr,
        color="darkorange",
        lw=lw,
        linestyle="-",
    )
    print("Kernel density plotted in " + str((time.time() - startTime) * 1000) + " ms")
    plt.show()

def evaluate(value, densityArr, max_value):
    X_plot = np.linspace(0, max_value, len(densityArr))[:, np.newaxis]
    result = np.interp(value, X_plot[:, 0], densityArr)
    return result