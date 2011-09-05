#!/usr/bin/env python
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor, task, protocol
try:
    import simplejson
except ImportError:
    import json as simplejson
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

class TcpEcho(protocol.Protocol):
    """This is just about the simplest possible protocol"""
    
    def dataReceived(self, data):
        "As soon as any data is received, write it back."
        self.transport.write("FROM JUGGLED\n")
        print data
        
        
log_file = None;
if len(sys.argv) >= 2:
    log_file = sys.argv[1];

myecho = Echo(log_file)

reactor.listenUDP(12345, myecho)

# listen to tcp
factory = protocol.ServerFactory()
factory.protocol = TcpEcho
reactor.listenTCP(12345,factory)

reactor.run()

