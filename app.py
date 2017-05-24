# -*- coding: utf-8 -*-
import sys,os
print('\nPython %s on %s\n' % (sys.version, sys.platform))
from flask import Flask, jsonify, request
import os
from core import worker
from rq import Queue
from rq.job import Job
import json
from datetime import datetime
import rq_dashboard

app = Flask(__name__)
app.config.from_object(rq_dashboard.default_settings)
app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rq")

c = worker.W.get_connection()
q = Queue(connection=c)

@app.route('/')
def index():
    # redis.incr('hits')
    return "Status: {}".format(datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S"))

@app.route('/jobs/<string:id>')
def job_status(id):
    job = Job.fetch(id, c)
    if job.is_finished:
        return 'Job {} finalizado'.format(id)
    else:
        return 'Ainda processando...'

@app.route('/jobs')
def jobs_list():
    d=[]
    for j in q.jobs:
        jd = j.to_dict()
        d.append({'id':j.id,'created_at':jd['created_at'],'enqueued_at':jd['enqueued_at'],'status':jd['status']})
    return json.dumps(d)

@app.route('/alerts/<start_date>/<end_date>')
def filter_alerts(start_date,end_date):
    return "Filter: {} - {}".format(start_date,end_date)

@app.route('/alerts/<alert_date>')
def get_alerts(alert_date):
    return "get_alerts: {} ".format(alert_date)

@app.route('/alerts/states/<alert_date>')
def get_states(alert_date):
    return "get_states: {} ".format(alert_date)

@app.route('/alerts/cities/<alert_date>')
def get_cities(alert_date):
    return "get_cities: {} ".format(alert_date)

@app.route('/alerts/report/<alert_date>')
def get_report(alert_date):
    return "get_report: {} ".format(alert_date)

@app.route('/alerts/symptoms/<symptoms>')
def get_alert_by_symptoms(symptoms):
    return "get_alert_by_symptoms: {} ".format(symptoms)

@app.route('/jobs/dropall/<key>')
def drop_jobs(key):
    if key == "sandman":
        q.empty()
        return "Corrent jobs: {}".format(q.count)
    return None

@app.route('/jobs/countall/<key>')
def count_jobs(key):
    if key == "sandman":
        return "Corrent jobs: {}".format(q.count)
    return None


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

