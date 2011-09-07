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

slice = 0.01

X=0
Y=1
Z=2

position     = [0, 0, 0]
acceleration = [0, 0, 0]
velocity     = [0, 0, 0]
key          = ['x', 'y', 'z']

n_points = 100
points   = [[0 for _ in range(0, n_points)], [0 for _ in range(0, n_points)], [0 for _ in range(0, n_points)]]

while True:
    try:
        ev, dt = logger.nextevent()
    except:
        break

    t = 0
    while t < dt:
        for axis in X, Y, Z:
            points[axis].append(position[axis] + velocity[axis] * slice)
            velocity[axis] += acceleration[axis] * slice
        t += slice

    e = simplejson.loads(ev)
    for axis in X, Y, Z:
        acceleration[axis] = e['data'][key[axis]]

    ax.plot(points[X][-1 * n_points:], points[Y][-1 * n_points:], points[Z][-1 * n_points:], 'r--')
    plt.draw()
