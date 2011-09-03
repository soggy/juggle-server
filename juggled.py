#!/usr/bin/env python
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

import simplejson

class Echo(DatagramProtocol):

    def datagramReceived(self, data, (host, port)):
        print "received %r from %s:%d" % (data, host, port)
        event_data = simplejson.loads(data);
        if event_data["type"] == "sensor_data":
            print event_data["data"]["x"], event_data["data"]["y"], event_data["data"]["z"]
        self.transport.write(data, (host, port))

reactor.listenUDP(12345, Echo())
reactor.run()
