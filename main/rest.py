from flask import Flask, jsonify, request, render_template
import logging
from main import poll_queue
import json

class statusEntry:
  '''Represents a consistent status entry'''
  def __init__(self, target="", status="", successes=0, failures=0):
    self.target = target 
    self.status = status
    self.successes = successes
    self.failures = failures

  def stat(self):
    formatted_output = {"status": self.status, "successes": self.successes, "failures": self.failures}
    return json.dumps(formatted_output)

def start_server():
  logging.debug("Trying to start Flask server")
  app = Flask(__name__)

  job_queue = []
  status_map = {}

  @app.route('/')
  def home():
    return render_template('index.html')

  @app.route('/health')
  def status():
    return jsonify('{"status": "ok"}')

  @app.route('/monitoring', methods=['GET'])
  def monitoring():
    logging.info(f"STATUS MAP: {status_map}")
    return render_template('monitoring.html', len=len(status_map), items=status_map)
    # queue_data = json.loads(poll_queue())
    # logging.debug(queue_data)
    # if queue_data:
    #   for site in queue_data:
    #     for site_name in site.keys():
    #       logging.debug(f"site_name is: {site_name}")
    #       name, target, interval = site_name, site[site_name]["target"], site[site_name]["interval"]
    #       status = cur_status[target]
    #       logging.debug(f"Values fetched are: {name} {target} {interval}")
    #   return(render_template('monitoring.html', job_names=site_name, target=target, interval=interval))
    # else:
    #   return("Empty Queue")

  @app.route('/stat', methods=['POST'])
  def update_status():
    data = request.json
    #if not data["target"] in status_map:
    entry = statusEntry(data["target"], data["status"], data["successes"], data["failures"])
    logging.info("CALLED")
    status_map = {entry.target: {entry.stat()}}
    #logging.info(f"Status map: {status_map}")


    return('', 201)

  @app.route('/clear-queue', methods=['PUT'])
  def clear_queue():
    job_queue = []

    return(jsonify(job_queue, 200))

  @app.route('/jobs')
  def get_jobs():
    return(jsonify(job_queue, 200))
  
  @app.route('/jobs', methods=['POST'])
  def add_job():
    data = request.get_json()
    logging.debug(f"Want to add {data} to queue")
    if not data in job_queue:
      job_queue.append(data)
      return('', 201)
    else:
      return('', 204)

  app.run()
