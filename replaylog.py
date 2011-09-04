import sys
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

import logger

class ReplayLog(DatagramProtocol):

    def __init__(self, log_file):
        self.log_file = log_file;
    
    def startProtocol(self):
        host = "127.0.0.1"
        port = 12345

        self.transport.connect(host, port)

        print "replaying log: %s" %(self.log_file);
        self.logger = logger.LoggerSender(self.log_file);
        self.logger.send_log(self.transport);

    def datagramReceived(self, data, (host, port)):
        print "received %r from %s:%d" % (data, host, port)

    # Possibly invoked if there is no server listening on the
    # address to which we are sending.
    def connectionRefused(self):
        print "No one listening"


log_file = None;
if len(sys.argv) >= 2:
    log_file = sys.argv[1];
    
# 0 means any port, we don't care in this case
reactor.listenUDP(8000, ReplayLog(log_file))
reactor.run()