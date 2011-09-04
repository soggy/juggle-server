#!/usr/bin/env python
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor, task
import simplejson
import sys

import logger

class Echo(DatagramProtocol):
    def __init__(self, log_file):
        self.phones = dict()
        #server = "192.168.1.1"
        #self.phones[server] = Phone(server)
        
        self.logger = None;
        if log_file:
            self.verbose = True
            self.logger = logger.Logger(log_file);
        else:
            self.verbose = False
            self.logger = logger.Logger(None)

    def datagramReceived(self, data, (host, port)):
        #print "received %r from %s:%d" % (data, host, port)
        if self.logger:
            self.logger.write(data);
            
        event_data = simplejson.loads(data)
        if self.verbose:
            print event_data, "from ", host, port
        #if event_data["type"] == "sensor_data":
        #    print event_data["data"]["x"], event_data["data"]["y"], event_data["data"]["z"]

log_file = None;
if len(sys.argv) >= 2:
    log_file = sys.argv[1];

myecho = Echo(log_file)

reactor.listenUDP(12345, myecho)
reactor.run()

