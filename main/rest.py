from flask import Flask, jsonify, request, render_template
import logging

def start_server():
  logging.debug("Trying to start Flask server")
  app = Flask(__name__)

  job_queue = []

  @app.route('/')
  def home():
    return render_template('index.html')

  @app.route('/jobs')
  def get_jobs():
    return jsonify(job_queue)
  
  @app.route('/jobs', methods=['POST'])
  def add_job():
    data = request.get_json()
    job_queue.append(data)

    return('', 204)

  app.run()
