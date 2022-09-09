import math
import fourier_discrete as fourier
import kernel_density as kdensity
import k_means as cluster

import datetime
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

MAX_SECONDS = (datetime.datetime(2018, 11, 23) - datetime.datetime(2017, 11, 1)).total_seconds()
MAX_DAYS = int((datetime.datetime(2018, 11, 23) - datetime.datetime(2017, 11, 1)).total_seconds() / (3600 * 24))
MAX_SECONDS_IN_DAY = 3600 * 24

def calculate_ps_time(key):
    current_time_arr = []
    for i, row in main_grp.get_group(key).iterrows():
        dt = datetime.datetime.strptime(row["time"], "%H:%M:%S")
        num_seconds = dt.second + dt.minute * 60 + dt.hour * 3600
        current_time_arr.append(num_seconds)

    current_dens = kdensity.calculate(current_time_arr, MAX_SECONDS_IN_DAY, 900, "gaussian")
    a_cos, b_sin = fourier.dft(np.linspace(0, MAX_SECONDS_IN_DAY, len(current_dens))[:, np.newaxis][:, 0], current_dens)
    ps = fourier.power_spec(a_cos, b_sin)
    print(key)
    fourier.analyze(np.linspace(0, MAX_SECONDS_IN_DAY, len(current_dens))[:, np.newaxis][:, 0], current_dens)
    """
    plt.close("all")
    fig = plt.figure("Test", constrained_layout=True)
    gs = fig.add_gridspec(1, 1)
    fourier.plot_powerspec(ps, fig.add_subplot(gs[0, 0]))
    plt.show()
    """
    return ps

def calculate_ps_days(key):
    current_time_arr = []
    for i, row in main_grp.get_group(key).iterrows():
        dt = datetime.datetime.strptime(row["date"], "%Y-%m-%d")
        num_days = (dt - datetime.datetime(2017, 11, 1)).total_seconds() / (3600 * 24)
        current_time_arr.append(num_days)

    current_dens = kdensity.calculate(current_time_arr, MAX_DAYS, MAX_DAYS, "gaussian")
    a_cos, b_sin = fourier.dft(np.linspace(0, MAX_DAYS, len(current_dens))[:, np.newaxis][:, 0], current_dens)
    ps = fourier.power_spec(a_cos, b_sin)
    print(key)
    fourier.analyze(np.linspace(0, MAX_DAYS, len(current_dens))[:, np.newaxis][:, 0], current_dens)
    """
    plt.close("all")
    fig = plt.figure("Test", constrained_layout=True)
    gs = fig.add_gridspec(1, 1)
    fourier.plot_powerspec(ps, fig.add_subplot(gs[0, 0]))
    plt.show()
    """
    return ps

def calculate_ps_month(key):
    current_time_arr = []
    for i, row in main_grp.get_group(key).iterrows():
        dt = datetime.datetime.strptime(row["date"], "%Y-%m-%d")
        num_days = (dt - datetime.datetime(dt.year, dt.month, 1)).total_seconds() / (3600 * 24)
        current_time_arr.append(num_days)

    current_dens = kdensity.calculate(current_time_arr, MAX_DAYS, MAX_DAYS, "gaussian")
    a_cos, b_sin = fourier.dft(np.linspace(0, MAX_DAYS, len(current_dens))[:, np.newaxis][:, 0], current_dens)
    ps = fourier.power_spec(a_cos, b_sin)
    print(key)
    fourier.analyze(np.linspace(0, MAX_DAYS, len(current_dens))[:, np.newaxis][:, 0], current_dens)
    """
    plt.close("all")
    fig = plt.figure("Test", constrained_layout=True)
    gs = fig.add_gridspec(1, 1)
    fourier.plot_powerspec(ps, fig.add_subplot(gs[0, 0]))
    plt.show()
    """
    return ps

def add_pts(ps):
    color = "#"+''.join([random.choice('0123456789ABCDEF') for i in range(6)])
    test_pts.append((range(len(ps)), ps, color))

main_df = pd.read_csv("./httpd.log", sep=" ")
main_grp = main_df.groupby(["cs-uri-stem", "cs-username"])
test_pts = []
[add_pts(calculate_ps_month(key)[:fourier.max_freq]) for index, key in enumerate([key for key in main_grp.groups.keys() if key[0] == "/financials.dll"]) if index < 5]

add_pts(calculate_ps_month(("/financials.dll", "Wade.Carlson"))[:fourier.max_freq])

"""
for i, row in test_df.iterrows():
    dt = datetime.datetime.strptime(row["date"] + "," + row["time"], "%Y-%m-%d,%H:%M:%S")
    num_seconds = (dt - datetime.datetime(2017, 11, 1)).total_seconds()
    test_time_arr.append(num_seconds)
"""

"""
plt.close("all")
fig = plt.figure("Test", constrained_layout=True)
gs = fig.add_gridspec(1, 1)
fourier.plot_powerspec(ps, fig.add_subplot(gs[0, 0]))
plt.show()
"""

"""
fig = plt.figure("Test")
gs = fig.add_gridspec(1, 1)
ax = fig.add_subplot(gs[0, 0])

key_press_event = fig.canvas.mpl_connect(
    "key_press_event", lambda event: cluster.on_key_press(event, ax, points, clusters)
)

clusters = cluster.init_clusters(6)
#points = cluster.init_points(range(fourier.max_freq), ps[:fourier.max_freq])
points = cluster.init_points(test_pts[0], test_pts[1])

cluster.init_assign(points, clusters)
cluster.plot(ax, points, clusters)
plt.show()
"""
[plt.scatter(pt[0], pt[1], c=pt[2]) for pt in test_pts]
plt.show()