#!/usr/bin/env python
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor, task
import simplejson
import sys
import numpy as np

import logger

class Echo(DatagramProtocol):
    def __init__(self, log_file):
        self.phones = dict()
        #server = "192.168.1.1"
        #self.phones[server] = Phone(server)
        
        self.logger = None;
        if log_file:        
            self.logger = logger.Logger(log_file);

    def datagramReceived(self, data, (host, port)):
        #print "received %r from %s:%d" % (data, host, port)

        if self.logger:
            self.logger.write(data);
            
        event_data = simplejson.loads(data)
        print event_data
        if event_data["type"] == "sensor_data":
            print event_data["data"]["x"], event_data["data"]["y"], event_data["data"]["z"]

log_file = None;
if len(sys.argv) >= 2:
    log_file = sys.argv[1];

myecho = Echo(log_file)

reactor.listenUDP(12345, myecho)
reactor.run()

