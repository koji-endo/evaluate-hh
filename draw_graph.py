import numpy as np
import matplotlib.pyplot as plt
import sys

argvs = sys.argv
argc = len(argvs)

if argc != 2:
    print 'arg error'
    quit()

masterfile = './runge_dt0010.txt'
targetfile = argvs[1]

print targetfile
data = np.loadtxt(targetfile, delimiter=',', skiprows=3)

time = data[:,0]
voltage = data[:,1]


plt.xlabel('Time [msec]')
plt.ylabel('Membrane Potential  [mV]')
plt.ylim([-90, 50])
plt.plot(time, voltage)
plt.show()
