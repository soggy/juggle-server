#!/usr/bin/env python
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

import simplejson

import gobject
import numpy as np
import matplotlib
matplotlib.use('GTKAgg')

import matplotlib.pyplot as plt

class Phone:
    def __init__(self, server):
        self.server = server
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        #self.line, = self.ax.plot(np.random.rand(10))
        self.data = (np.ndarray(100), np.ndarray(100), np.ndarray(100))
        self.line, = self.ax.plot(self.data[0])
        self.ax.set_ylim(0, 1)

    def adddata(self, d):
        self.data[0][:-1] = self.data[0][1:]
        self.data[0][-1] = d["data"]["x"]
        
    def update(self):
        self.line.set_ydata(self.data[0])
        self.fig.canvas.draw_idle()

class Echo(DatagramProtocol):
    def __init__(self):
        self.phones = dict()
        #server = "192.168.1.1"
        #self.phones[server] = Phone(server)
        gobject.timeout_add(100, self.update)

    def datagramReceived(self, data, (host, port)):
        print "received %r from %s:%d" % (data, host, port)
        if host not in self.phones:
            self.phones[host] = Phone(host)
        phone = self.phones[host]
        event_data = simplejson.loads(data);
        if event_data["type"] == "sensor_data":
            print event_data["data"]["x"], event_data["data"]["y"], event_data["data"]["z"]
            phone.adddata(event_data)
        #self.transport.write(data, (host, port))

    def update(self):
        for phone in self.phones.values():
            phone.update()
        return True # False terminates updates

reactor.listenUDP(12345, Echo())
plt.show()
reactor.run()

