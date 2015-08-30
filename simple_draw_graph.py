import numpy as np
import matplotlib.pyplot as plt
import sys

argvs = sys.argv
argc = len(argvs)

masterfile = './hh_cnexp_0200.txt'
targetfile = './hh_euler_0200.txt'

print targetfile
data = np.loadtxt(targetfile, delimiter=',', skiprows=3)
data2 = np.loadtxt(masterfile, delimiter=',', skiprows=3)
#data3 = np.loadtxt(targetfile, delimiter=',', skiprows=3)

time = data[:,0]
voltage = data[:,1]


plt.xlabel('Time [msec]')
plt.ylabel('Membrane Potential  [mV]')
plt.ylim([-90, 50])
plt.plot(time, voltage)
plt.plot(data2[:,0], data2[:,1])
plt.show()
