import sys
import numpy as np
import matplotlib.pyplot as plt
import neuron

def calc_hh(dt = 0.025, method='cnexp', show_plot=False):

    filename_template = 'hh_%s_%04d.txt'
    filename = filename_template % (method, int(dt*1000))

    h = neuron.hoc.HocObject()
    h('nrn_load_dll("./mod/x86_64/.libs/libnrnmech.so")')

    soma = neuron.h.Section(name="soma")
    
    soma.nseg = 3    # odd number
    soma.diam = 10   # [um]
    soma.L = 10      # [um]
    
    if method == 'cnexp':
        soma.insert("hh_cnexp")
        meca = soma(0.5).hh_cnexp
    elif method == 'impl':
        soma.insert("hh_impl")
        meca = soma(0.5).hh_impl
    elif method == 'euler':
        soma.insert("hh_euler")
        meca = soma(0.5).hh_euler
    elif method == 'runge':
        soma.insert("hh_runge")
        meca = soma(0.5).hh_runge
    else:
        print 'wrong method.'
        quit()


    stim = neuron.h.IClamp(soma(0.5))
    stim.delay = 50  # [ms]
    stim.dur = 200   # [ms]
    stim.amp = 0.15  # [nA]
    
    
    rec_t = neuron.h.Vector()
    rec_t.record(neuron.h._ref_t)
    
    rec_v = neuron.h.Vector()
    rec_v.record(soma(0.5)._ref_v)
    
    neuron.h.finitialize(-65)
    tstop = 300
    neuron.h.dt = float(dt)
    neuron.run(tstop)
    print "dt = %f" % neuron.h.dt
    
    # convert neuron array to numpy array
    time = rec_t.as_numpy()
    voltage = rec_v.as_numpy()


    f = open(filename, 'w')
    for i in range(len(time)):
        f.write("%d, %f\n" % (int(time[i]*1000), voltage[i]))
    f.close()


    # show graph by matplotlib
    if show_plot == True:
        plt.plot(time, voltage, color='b')
        plt.xlabel("Time [ms]")
        plt.ylabel("Voltage [mV]")
        plt.axis(xmin=0, xmax=max(time), ymin=min(voltage)-5, ymax=max(voltage)+5)
        plt.show()


if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)

    if argc == 3:
        calc_hh(dt=float(argvs[1]), method=argvs[2])
    else:
        print 'arg error.'

    
