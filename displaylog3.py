#!/usr/bin/env python

import sys
try:
    import simplejson
except ImportError:
    import json as simplejson
import logger

import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

log_file = None
if len(sys.argv) >= 2:
    log_file = sys.argv[1]

logger = logger.LoggerSender(log_file)
logger.dosleeps = False

fig = plt.figure()
ax = Axes3D(fig)

xs = []
ys = []
zs = []
while 1:
    try:
        e = simplejson.loads(logger.nextevent())
    except:
        break

    xs.append(e['data']['x'])
    ys.append(e['data']['y'])
    zs.append(e['data']['z'])

    # ax.plot(xs, ys, zs)
    # plt.draw()

ax.plot(xs, ys, zs)
plt.show()
