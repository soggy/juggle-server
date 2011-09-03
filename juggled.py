#!/usr/bin/env python
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

import gobject
import numpy as np
import matplotlib
matplotlib.use('GTKAgg')

class Phone:
    def __init__(self):
        self.ip = ip
        self.port = port
        self.fig = plt.figure()
        self.ax = fig.add_subplot(111)
        self.line, = self.ax.plot(np.random.rand(10))
        self.ax.set_ylib(0, 1)

    def update():
        line.set_ydata(np.random.rand(10))
        self.fig.canvas.draw_idle()

class Echo(DatagramProtocol):
    def __init__(self):
        self.phones = dict()
        gobject.timeout_add(100, self.update)

    def datagramReceived(self, data, (host, port)):
        print "received %r from %s:%d" % (data, host, port)
        self.transport.write(data, (host, port))

    def update():
        for phone in self.phones:
            phone.update()
        return True # False terminates updates

reactor.listenUDP(12345, Echo())
reactor.run()
plt.show()

