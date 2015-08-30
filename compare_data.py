import numpy as np
import matplotlib.pyplot as plt
import sys
import math

class CompareData():
    
    
    def __init__(self, targetfile='./result/hh_cnexp_0100.txt', masterfile='./result/hh_runge_0020.txt'):
    
        print targetfile
        self.targetfile=targetfile
        self.masterfile=masterfile
        self.target = np.loadtxt(targetfile, delimiter=',', skiprows=3)
        self.master = np.loadtxt(masterfile, delimiter=',', skiprows=3)
        self.fontsize=20

    def _cutoff(self, val):
        return int((val+1) / 10) * 10

    def compare_data(self):
        target_pos = 0
        self.sub = []

        for record in self.master:
            #print record[0]
            if self._cutoff(record[0]) == self._cutoff(self.target[target_pos, 0]):
                self.sub.append(math.fabs(record[0] - self.target[target_pos, 0]))
                if target_pos+1 < len(self.target):
                    target_pos += 1
                
        print self.sub
        

    def draw_graph(self):
        target_time = self.target[:,0]
        target_voltage = self.target[:,1]
        master_time = self.master[:,0]
        master_voltage = self.master[:,1]
        
        
        plt.plot(master_time, master_voltage, color='#aa3333', lw=2, label=self.masterfile)
        plt.plot(target_time, target_voltage, color='k', linestyle='-', lw=1, label=self.targetfile)
        plt.xticks(fontsize=self.fontsize*0.8)
        plt.yticks(fontsize=self.fontsize*0.8)
        plt.xlabel('Time [micro sec]', fontsize=self.fontsize)
        plt.ylabel('Membrane Potential  [mV]', fontsize=self.fontsize)
        plt.ylim([-90, 50])
        plt.xlim([0, 300000])
        plt.legend(fontsize=16)
        plt.grid(True)
        #plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    
    cmp = CompareData()
    cmp.draw_graph()
    cmp.compare_data()
    