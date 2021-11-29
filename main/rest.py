from flask import Flask, jsonify, request, render_template
import logging
from main import poll_queue
import json

def start_server():
  logging.debug("Trying to start Flask server")
  app = Flask(__name__)

  job_queue = []

  @app.route('/')
  def home():
    return render_template('index.html')

  @app.route('/health')
  def status():
    return jsonify('{"status": "ok"}')

  @app.route('/monitoring', methods=['GET'])
  def monitoring():
    queue_data = json.loads(poll_queue())
    logging.debug(queue_data)
    #sites = {}
    for site in queue_data:
      for site_name in site.keys():
        logging.debug("site_name is: {}".format(site_name))
        name, target, interval = site_name, site[site_name]["target"], site[site_name]["interval"]
        logging.debug("Values fetched are: {} {} {}".format(name, target, interval))
    return render_template('monitoring.html', job_names=site_name, target=target, interval=interval)

  @app.route('/stat', methods=['POST'])
  def update_status():
    print(request.json)
    data = request.json
    site_name, status = data["name"], data["status"]
    cur_status = {}
    cur_status[site_name] = status

    return('', 201)

  @app.route('/jobs')
  def get_jobs():
    return jsonify(job_queue)
  
  @app.route('/jobs', methods=['POST'])
  def add_job():
    data = request.get_json()
    job_queue.append(data)

    return('', 204)

  app.run()
