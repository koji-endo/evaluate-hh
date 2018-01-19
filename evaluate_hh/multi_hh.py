import sys
import numpy as np
import matplotlib.pyplot as plt
import neuron


def calc_hh(dt = 25, method='cnexp', show_plot=False, type=0):
    """
    dt = (int) [micro sec]
    method = cnexp | impl | euler | runge
    show_plot = True | False
    """

    filename_template = './multi_result/hh_%d.txt'
    filename = filename_template % type

    if type == 0:
        pos_list = [331, 553, 1087, 2222, 3838]
    elif type == 1:
        pos_list = [290, 488, 955, 1684, 2820]
    elif type == 2:
        pos_list = [44, 76, 131, 439, 846]
    elif type == 3:
        pos_list = [26, 42, 64, 201, 366]
    elif type == 4:
        pos_list = [10, 15, 23, 101, 184]

    h = neuron.hoc.HocObject()
    h.execute('type = '+str(type))
    h('nrn_load_dll("./mod/x86_64/.libs/libnrnmech.so")')
    neuron.h.load_file('swc_main.hoc')

    for sec in h.allsec():
        if method == 'cnexp':
            sec.insert("hh_cnexp")
            meca = sec(0.5).hh_cnexp
        elif method == 'impl':
            sec.insert("hh_impl")
            meca = sec(0.5).hh_impl
        elif method == 'euler':
            sec.insert("hh_euler")
            meca = sec(0.5).hh_euler
        elif method == 'runge':
            sec.insert("hh_runge")
            meca = sec(0.5).hh_runge
        else:
            print('wrong method.')
            quit()

        sec.nseg = 1
        # neuron.h.psection()

    stim = neuron.h.IClamp(h.CellSwc[0].Dend[pos_list[0]](0.5))
    stim.delay = 50  # [ms]
    stim.dur = 200   # [ms]
    stim.amp = 0.10  # [nA]
    
    rec_t = neuron.h.Vector()
    rec_t.record(neuron.h._ref_t)
    
    rec_v1 = neuron.h.Vector()
    rec_v1.record(h.CellSwc[0].Dend[pos_list[1]](0.5)._ref_v)
    rec_v2 = neuron.h.Vector()
    rec_v2.record(h.CellSwc[0].Dend[pos_list[2]](0.5)._ref_v)
    rec_v3 = neuron.h.Vector()
    rec_v3.record(h.CellSwc[0].Dend[pos_list[3]](0.5)._ref_v)
    rec_v4 = neuron.h.Vector()
    rec_v4.record(h.CellSwc[0].Dend[pos_list[4]](0.5)._ref_v)
    
    neuron.h.finitialize(-65)
    tstop = 300
    neuron.h.dt = float(dt)/1000.
    # neuron.h.secondorder = 2
    neuron.run(tstop)
    print("dt = %f" % neuron.h.dt)
    
    # convert neuron array to numpy array
    time = rec_t.as_numpy()
    voltage1 = rec_v1.as_numpy()
    voltage2 = rec_v2.as_numpy()
    voltage3 = rec_v3.as_numpy()
    voltage4 = rec_v4.as_numpy()

    with open(filename, 'w') as f:
        f.write('# %s\n' % filename)
        f.write('# dt = %d [usec]\n' % dt)
        f.write('# t [usec], V [mV]\n')
        for i in range(len(time)):
            # checked_time = int((int(time[i]*10000)+1)/10) * 10
            checked_time = int((int(time[i]*1000)+1)/10) * 10
            # checked_time = int(time[i]*1000)
            f.write("%d, %f, %f, %f, %f\n" % (checked_time, voltage1[i], voltage2[i], voltage3[i], voltage4[i]))

    # show graph by matplotlib
    if show_plot:
        plt.plot(time, voltage1, color='b')
        plt.xlabel("Time [ms]")
        plt.ylabel("Voltage [mV]")
        plt.axis(xmin=0, xmax=max(time), ymin=min(voltage)-5, ymax=max(voltage)+5)
        plt.show()


if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)

    if argc == 2:
        calc_hh(type=int(argvs[1]))
