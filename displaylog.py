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

log_file = None
if len(sys.argv) >= 2:
    log_file = sys.argv[1]

print "hi"
logger = logger.LoggerSender(log_file);
linedata = np.random.rand(100)
fig = plt.figure()
ax = fig.add_subplot(111)
line, = ax.plot(linedata)
ax.set_ylim(-10, 10)

def update():
    e = simplejson.loads(logger.nextevent())
    linedata[:-1] = linedata[1:]
    linedata[-1] = np.float64(e["data"]["x"])
    #linedata[50] = e["data"]["x"]
    ld = np.random.rand(100)
    #ld[0] = np.float64(linedata[0])
    #ld = linedata.copy() #np.ndarray(100)
    for i in xrange(0, len(linedata)-1):
        ld[i] = np.float64(linedata[i])
    #print type(ld[0])
    print ld
    #print linedata
    #line, = ax.plot(ld)
    #line.set_ydata(linedata)
    line.set_ydata(ld)
    fig.canvas.draw()
    return True

gobject.timeout_add(100, update)
plt.show()
