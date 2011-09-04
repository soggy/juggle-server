#!/usr/bin/python

import sys, time
import simplejson
import logger

import gobject
import numpy as np
import gtk
import matplotlib
matplotlib.use('GTKAgg')
import matplotlib.pyplot as plt

class AccelViewer:
    def __init__(self, filename, samples):
        self.logger = logger.LoggerSender(filename)
        self.samples = samples
        self.linedata = {"x": np.ndarray(samples),
                         "y": np.ndarray(samples),
                         "z": np.ndarray(samples)}
        for key in self.linedata.keys():
            for i in xrange(0, len(self.linedata[key])):
                self.linedata[key][i] = 0.0
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.lines = {"x": self.ax.plot(self.linedata["x"])[0],
                      "y": self.ax.plot(self.linedata["y"])[0],
                      "z": self.ax.plot(self.linedata["z"])[0]}
        self.ax.set_ylim(-20, 20)

    def shiftandappend(self, event):
        # Apparently slices don't work.  WTF?
        # ld[:-1] = linedata[1:]
        # ld[-1] = np.float64(e["data"]["x"])
        for key in self.linedata.keys():
            nd = np.ndarray(self.samples)
            for i in xrange(0, self.samples-1):
                nd[i] = self.linedata[key][i+1]
            nd[-1] = event["data"][key]
            self.linedata[key] = nd

    def update(self):
        e = simplejson.loads(self.logger.nextevent())
        self.shiftandappend(e)
        for key in self.linedata.keys():
            self.lines[key].set_ydata(self.linedata[key])
        self.fig.canvas.draw()
        return True

log_file = None
if len(sys.argv) >= 2:
    log_file = sys.argv[1]

view = AccelViewer(log_file, 200)
gobject.idle_add(view.update)
plt.show()
