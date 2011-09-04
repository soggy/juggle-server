#!/usr/bin/env python
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor, task

import simplejson

import sys

import logger

class Phone:
    def __init__(self, server):
        self.server = server

class Echo(DatagramProtocol):
    def __init__(self, log_file):
        self.phones = dict()
        server = "192.168.1.117"
        self.phones[server] = Phone(server)
        
        self.logger = None;
        if log_file:        
            self.logger = logger.Logger(log_file);

        print "I'm awake..."

    def datagramReceived(self, data, (host, port)):
        print "received %r from %s:%d" % (data, host, port)
        if self.logger:
            self.logger.write(data);
            
        event_data = simplejson.loads(data);		
        if event_data["type"] == "sensor_data":
            print event_data["data"]["x"], event_data["data"]["y"], event_data["data"]["z"]
        self.transport.write(data, (host, port))

    def update(self):
        for phone in self.phones.values():
            phone.update()
        return True # False terminates updates

log_file = None;
if len(sys.argv) >= 2:
    log_file = sys.argv[1];

reactor.listenUDP(12345, Echo(log_file))
reactor.run()

