import matplotlib.pyplot as plt
import numpy as np
import load

def n_ln(dist, numbins):
    log_dist = np.log10(dist)
    bins = np.linspace(min(log_dist),max(log_dist), numbins)
    hist, r_array = np.histogram(log_dist, bins)

    dR = r_array[1]-r_array[0]    
    x_array = r_array[1:] - dR/2
    volume =  [4.*np.pi*i**3. for i in 10**x_array[:] ]

    return [10**x_array, hist/dR/volume]

plt.style.use('seaborn-whitegrid')

data = np.array(load.LoadLogFile())
result = n_ln(data[:,1], 284200)
print(result)

#here's our data to plot, all normal Python lists
x = data[:,1]
y = np.full((284200, 1), 0)

#intensity = np.full((284200, 1), 1)

#setup the 2D grid with Numpy
#x, y = np.meshgrid(x, y)

#now just plug the data into pcolormesh, it's that easy!
#plt.pcolormesh(x, y, intensity)
#plt.colorbar() #need a colorbar to show the intensity scale
plt.plot(x,y)
plt.show() #boom