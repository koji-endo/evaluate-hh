import numpy as np
import matplotlib.pyplot as plt
import sys
import math

class CompareData():
    
    FILETEMPLATE = './result/hh_%s_%04d.txt'
    MASTER_METHOD = 'runge'
    MASTER_DT = 1
    IMAGE_POS = './images/'
    
    def __init__(self, method='runge', dt=10, compare_method=1, draw_fig=False):
    
        targetfile = self.FILETEMPLATE % (method, dt)
        masterfile = self.FILETEMPLATE % (self.MASTER_METHOD, self.MASTER_DT)

        self.targetfile=targetfile
        self.masterfile=masterfile
        self.target = np.loadtxt(targetfile, delimiter=',', skiprows=3)
        self.master = np.loadtxt(masterfile, delimiter=',', skiprows=3)
        self.fontsize=20
        self.method=method
        self.dt=dt
        self.draw_fig=draw_fig
        self.compare_method=compare_method
        self.title_table = {'euler':'Euler Method', 'impl':'Backward Euler Method', 'runge':'Runge-Kutta 4th-Order Method', 'cnexp':'Exponential Integrator Method'}

    def _cutoff(self, val):
        return int((val+1) / 10) * 10

    def compare_data(self):
        target_pos = 0
        self.sub = []

        for (i, record) in enumerate(self.master):
            if record[0] == self.target[target_pos, 0]:
                value = record[1] - self.target[target_pos, 1]
               
                if len(self.sub) != 0:
                    if self.compare_method == 1:
                        self.sub.append( value * (self.target[target_pos, 0] - self.target[target_pos-1, 0]))
                    elif self.compare_method == 2:
                        self.sub.append( value * (self.target[target_pos, 0] - self.target[target_pos-1, 0]) + self.sub[-1])
                    else:
                        print 'Wrong Compare Method.'
                        return
                else:
                    self.sub.append(0)
                                        
                if target_pos+1 < len(self.target):
                    target_pos += 1

        abs_sub = []           
        for x in self.sub:
            abs_sub.append(math.fabs(x))

        total_error = math.fsum(abs_sub)
        print '%s (%5d [usec]) - %s (%5d [usec]) : %10.1f (%5d)' % (self.method, self.dt, self.MASTER_METHOD, self.MASTER_DT, total_error, target_pos)
        return total_error
        

    def draw_graph(self):
        target_time = self.target[:,0]
        target_voltage = self.target[:,1]
        master_time = self.master[:,0]
        master_voltage = self.master[:,1]
        
        
        plt.plot(master_time, master_voltage, color='#aa3333', lw=3, label=self.title_table[self.MASTER_METHOD] + (' (dt = %d)' % self.MASTER_DT) + r'[$\mathrm{\mu sec}$]')
        plt.plot(target_time, target_voltage, color='k', linestyle='-', lw=1, label=self.title_table[self.method] + (' (dt = %d)' % self.dt) + r'[$\mathrm{\mu sec}$]')
        plt.xticks(fontsize=self.fontsize*0.8)
        plt.yticks(fontsize=self.fontsize*0.8)
        plt.xlabel(r'$\mathrm{ Time [\mu sec]}$', fontsize=self.fontsize)
        plt.ylabel(r'$\mathrm{Membrane Potential [mV]}$', fontsize=self.fontsize)
        plt.ylim([-90, 80])
        plt.xlim([0, 300000])
        plt.legend(fontsize=16)
        plt.grid(True)
        #plt.tight_layout()
        
        plt.savefig(self.IMAGE_POS+'hh_'+self.method+'_'+('%04d' % self.dt)+'.png', figsize=(20, 20), dpi=300)
        plt.show()




def compare_all():
    compare_method = 1   # 1 or 2
    draw_graph = False   # True or False
    result_all = {
        'euler_title':'Euler Method',
        'impl_title':'Backward Euler Method',
        'runge_title':'Runge-Kutta 4th-Order Method',
        'cnexp_title':'Exponential Integrator Method'
    }
    
    for method in ['euler', 'impl', 'runge', 'cnexp']:
        result_dt = []
        result_error = []
        for i in range(10, 1000, 10):
            cmp = CompareData(method=method, dt=i, compare_method=compare_method)
            if draw_graph:
                cmp.draw_graph()

            result_dt.append(i)
            result_error.append(cmp.compare_data())
    
        result_all[method+'_dt'] = result_dt
        result_all[method+'_error'] = result_error
    
    
    for method in ['euler', 'impl', 'runge', 'cnexp']:
        plt.plot(result_all[method+'_dt'], result_all[method+'_error'], label=result_all[method+'_title'], lw=2)

    fontsize = 18

    plt.xlabel(r'$\mathrm{Discrete Time \ \ [\mu sec]}$', fontsize=fontsize)
    if compare_method == 1:
        plt.ylabel(r'$\int \ |T(t) - R(t) | dt \ \ \mathrm{[ mV \cdot \mu sec ]}$', fontsize=fontsize)
        #plt.xlim([0, 200])
        #plt.ylim([0, 1000000])
        plt.ylim([0, 6000000])
        #plt.ylim([100000, 10000000])
        plt.legend(fontsize=fontsize*0.8, loc=4)
        #plt.yscale('log')
    elif compare_method == 2:
        plt.ylabel(r'$\int_0^{t\mathrm{max}} \ \left| \int_0^a T(t) - R(t)  dt \right| da \ \ \mathrm{[ mV \cdot \mu sec ]}$', fontsize=fontsize)
        plt.ylim([0, 100000000])
        plt.legend(fontsize=fontsize*0.8, loc=1)
    else:
        print 'Wrong Compare Method'
        
    plt.axvline(x=25, color='k', linestyle=':')
    plt.axvline(x=50, color='k', linestyle=':')
    plt.xticks(fontsize=fontsize*0.8)
    plt.yticks(fontsize=fontsize*0.8)
    plt.grid(True)
    plt.show()




if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    
    compare_all()
    '''
    cmp = CompareData(method='euler', dt=100)
    cmp.compare_data()
    cmp.draw_graph()
    '''

