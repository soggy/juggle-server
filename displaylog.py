#!/usr/bin/env python

import os, sys, time, math
try:
    import simplejson
except ImportError:
    import json as simplejson
import logger, transform

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def beep():
    f=open('/dev/tty','w')
    f.write(chr(7))
    f.close() 

class AccelViewer:
    def __init__(self, filename, samples, onlymagnitude):
        self.logger = logger.LoggerSender(filename)
        # self.logger.dosleeps = False
        self.samples = samples
        self.linedata = {"x": np.ndarray(samples),
                         "y": np.ndarray(samples),
                         "z": np.ndarray(samples)}
        # FIX: presumably numpy has a "zero" method
        for key in self.linedata.keys():
            for i in xrange(0, len(self.linedata[key])):
                self.linedata[key][i] = 0.0
        self.magdata = np.ndarray(samples)
        self.deltatimes = np.ndarray(samples)
        for i in xrange(0, len(self.magdata)):
            self.magdata[i] = 0.0
            self.deltatimes[i] = 0.0
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.onlymagnitude = onlymagnitude
        self.lines = dict()
        if not self.onlymagnitude:
            self.lines["x"] = self.ax.plot(self.linedata["x"])[0]
            self.lines["y"] = self.ax.plot(self.linedata["y"])[0]
            self.lines["z"] = self.ax.plot(self.linedata["z"])[0]
        self.magline, = self.ax.plot(self.magdata)
        self.ax.set_ylim(0, 35)

    def shiftandappend(self, deltatime, event):
        # Apparently slices don't work.  WTF?
        # ld[:-1] = linedata[1:]
        # ld[-1] = np.float64(e["data"]["x"])
        newmag = 0.0 # going to be sqrt(sum(sqr(x, y, z))) values
        for key in self.linedata.keys():
            nd = np.ndarray(self.samples)
            for i in xrange(0, self.samples-1):
                nd[i] = self.linedata[key][i+1]
            v = event["data"][key]
            nd[-1] = v
            newmag += v*v
            self.linedata[key] = nd
        nd = np.ndarray(self.samples)
        ndd = np.ndarray(self.samples)
        for i in xrange(0, self.samples-1):
            nd[i] = self.magdata[i+1]
            ndd[i] = self.deltatimes[i+1]
        # nd[-1] = math.sqrt(newmag) - 9.8
        nd[-1] = math.sqrt(newmag)
        ndd[-1] = deltatime
        self.magdata = nd
        self.deltatimes = ndd

    def inflection(self, n):
        L = len(self.magdata)
        A = 0.0
        B = 0.0
        for i in xrange(L-1, L-n-1, -1):
            #print i, self.magdata[i], self.magdata[i-1], self.deltatimes[i]
            B += ((self.magdata[i] - self.magdata[i-1]) / self.deltatimes[i])
        B /= float(n)
        for i in xrange(L-n-1, L-(2*n)-1, -1):
            #print i, self.magdata[i], self.magdata[i-1], self.deltatimes[i]
            A += ((self.magdata[i] - self.magdata[i-1]) / self.deltatimes[i])
        A /= float(n)
        #print "inflection test: ", A, B
        if (math.fabs(A - B) < 50):
            return
        if (A > 0 and B < 0):
            print "TURNED DOWN", A, B
            beep()
            #os.system('echo -e "\007"')
            #os.system("mplayer /usr/share/sounds/KDE-Im-Message-In.ogg &")
        if (A < 0 and B > 0):
            print "TURNED UP", A, B
            beep()
            #os.system('echo -e "\007"')

    def update(self):
        (e, dt) = self.logger.nextevent()
        e = simplejson.loads(e)
        #print "deltat", dt
        accel = (e["data"]["x"], e["data"]["y"], e["data"]["z"])
        orient = (e["data"]["azimuth"], e["data"]["pitch"], e["data"]["roll"])
        #A = transform.phone2world(accel, orient)
        #print "worldcoords: ", A
        self.shiftandappend(dt, e)
        self.inflection(2)
        if not self.onlymagnitude:
            for key in self.linedata.keys():
                self.lines[key].set_ydata(self.linedata[key])
        self.magline.set_ydata(self.magdata)
        self.fig.canvas.draw()
        return True

log_file = None
if len(sys.argv) >= 2:
    log_file = sys.argv[1]

view = AccelViewer(log_file, 200, True)
while True:
    view.update()
plt.show()
