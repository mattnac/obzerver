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
  target = ""
  interval = 0
  is_https = ""

  if target == None or interval == None or is_https == None:
    logging.error("Missing environment variables.")

  os.environ['FLASK_APP'] = 'rest.py'

  logging.info("Starting REST API")
  rest_int = threading.Thread(target=rest.start_server, daemon=True).start()
  while True:
    curr_queue = list(poll_queue())
    logging.info(f"Queue is: {curr_queue}")
    while len(curr_queue) > 0:
      item = curr_queue.pop()
      target, interval = item["target"], item["interval"]
      is_https = True if "true" or "TRUE" in is_https else False
      logging.info(f"Starting job for {target}")
      job = threading.Thread(target=run, args=(target, interval, is_https)).start()
      logging.info(f"queue length is {len(curr_queue)}")
      if len(curr_queue) == 0:
        requests.put('http://127.0.0.1:5000/clear-queue')

    time.sleep(5)

def run(target, interval, is_https):
  logging.debug("In run function.")
  # is_https = True if "true" or "TRUE" in is_https else False
  # if "true" or "TRUE" in is_https:
  #   is_https = True
  # else:
  #   is_https = False

  run_url = urlformat.urlformat(target, is_https)
  client = create_client(run_url, interval, is_https)
  job = client.daemonize()
  
  return(job)

def create_client(run_url, interval, is_https):
  logging.debug("Creating client")
  run_client = daemon.Daemon(run_url, interval, is_https)
  return run_client

def poll_queue():
  job_queue = requests.get('http://127.0.0.1:5000/jobs')
  return(job_queue.json()[0])

if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  main()