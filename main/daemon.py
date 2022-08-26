import requests
import time
import logging
import sys
import requests

class Daemon():
    def __init__(self, target, interval, is_https):
        self.target = target
        self.interval = interval
        self.is_https = is_https
    
    def daemonize(self):
        success = 0
        failure = 0
        while self.target is not None:
            #try:
            logging.debug("Firing of request to {}".format(self.target))
            r = requests.get(self.target)
            if r.status_code >= 200 and r.status_code < 300:
                success += 1
                requests.post('http://127.0.0.1:5000/stat', json={"target": self.target, "status": "up", "successes": success, "failures": failure})
            else:
                failure += 1
                requests.post('http://127.0.0.1:5000/stat', json={"target": self.target, "status": "down", "successes": success, "failures": failure})
            logging.debug("Request fired, sleeping for interval")
            time.sleep(self.interval)
          #except:
            #logging.error("Something went wrong with sending the request.")
            #sys.exit(1)