import os
import urlformat
import daemon
import threading
import logging
import rest
import requests
import json
import time

def main():    
  target = None
  interval = 0
  is_https = ""
  if target == None or interval == None or is_https == None:
    logging.error("Missing environment variables.")

  logging.debug("About to execute run function.")
  os.environ['FLASK_APP'] = 'rest.py'

  logging.debug("Starting thread #1")
  rest_int = threading.Thread(target=rest.start_server, daemon=True).start()
  while target is None:
    logging.debug("In loop")
    queue = json.loads(poll_queue())
    time.sleep(5)

    for item in queue:
      job_name = list(item.keys())
      target, interval = item[job_name[0]]["target"], item[job_name[0]]["interval"]
      is_https = True
      logging.debug("Starting job for {}".format(target))
      job = threading.Thread(target=run, args=(target, interval, is_https)).start()


def run(target, interval, is_https):
  logging.debug("In run function.")
  if "true" or "TRUE" in is_https:
    is_https = True
  else:
    is_https = False

  run_url = urlformat.urlformat(target, is_https)
  client = create_client(run_url, interval, is_https)
  job = client.daemonize()

def create_client(run_url, interval, is_https):
  logging.debug("Creating client")
  run_client = daemon.Daemon(run_url, interval, is_https)
  return run_client

def poll_queue():
  job_queue = requests.get('http://127.0.0.1:5000/jobs')
  return(job_queue.text)

if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  main()