import time
import simplejson

class Logger:
   def __init__(self, file_name):
       self.log_file = open(file_name, "wb");
       self.start_time = time.time();
	   
   def write(self, event):
       log_event = {"time": time.time() - self.start_time, "event": event}
       self.log_file.write("%s\n" % simplejson.dumps(log_event));
	   
       
class LoggerSender:
    def __init__(self, file_name):
        self.log_file = open(file_name, "rb");
        self.last_time = 0.0;
            
    def send_log(self, transport):
        for line in self.log_file:
            event = simplejson.loads(line);            
            
            # sleep for the differnce in time between the time in the current event, and the last_time
            cur_time = float(event["time"])
            if not self.last_time:
                self.last_time = cur_time;
                
            time.sleep(cur_time - self.last_time);
            
            transport.write(event["event"])
            
            print event["time"], event["event"]
        