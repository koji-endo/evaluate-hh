import numpy as np
import matplotlib.pyplot as plt
import sys

argvs = sys.argv
argc = len(argvs)

#masterfile = './hh_cnexp_0200.txt'
targetfile0 = './multi_result/hh_0.txt'
targetfile1 = './multi_result/hh_1.txt'
targetfile2 = './multi_result/hh_2.txt'
targetfile3 = './multi_result/hh_3.txt'
targetfile4 = './multi_result/hh_4.txt'

print targetfile
data0 = np.loadtxt(targetfile0, delimiter=',', skiprows=3)
data1 = np.loadtxt(targetfile1, delimiter=',', skiprows=3)
data2 = np.loadtxt(targetfile2, delimiter=',', skiprows=3)
data3 = np.loadtxt(targetfile3, delimiter=',', skiprows=3)
data4 = np.loadtxt(targetfile4, delimiter=',', skiprows=3)
#data2 = np.loadtxt(masterfile, delimiter=',', skiprows=3)
#data3 = np.loadtxt(targetfile, delimiter=',', skiprows=3)

'''
time = data0[:,0]
voltage1 = data0[:,1]
voltage2 = data0[:,2]
voltage3 = data0[:,3]
voltage4 = data0[:,4]
'''

for (i,data) in enumerate([data0, data1, data2, data3, data4]):
    time = data[:,0]
    voltage1 = data[:,1]
    voltage2 = data[:,2]
    voltage3 = data[:,3]
    voltage4 = data[:,4]
    
    fontsize=20
    
    plt.plot(time, voltage1, label='M1')
    plt.plot(time, voltage2, label='M2')
    plt.plot(time, voltage3, label='M3')
    plt.plot(time, voltage4, label='M4')
    
    plt.xticks(fontsize=fontsize*0.8)
    plt.yticks(fontsize=fontsize*0.8)
    plt.xlabel(r'$\mathrm{ Time [\mu sec]}$', fontsize=fontsize)
    plt.ylabel(r'$\mathrm{Membrane Potential [mV]}$', fontsize=fontsize)
    plt.ylim([-90, 60])
    plt.xlim([0, 300000])
    plt.legend(fontsize=fontsize*0.8, ncol=4)
    plt.grid(True)
     
    #plt.plot(data2[:,0], data2[:,1])
    plt.savefig('multi'+str(i)+'.png', figsize=(20, 20), dpi=300)
    plt.show()
