from flask import Flask, render_template, jsonify, abort
from flask_socketio import SocketIO, emit

import settings
from models import db
from reports import validate_report, json_report

app = Flask(__name__)
app.config.from_object(settings)
socketio = SocketIO(app)
db.init_app(app)


@app.route('/')
def overview():
    return render_template('overview.html')


@app.route('/socketio-test')
def socketio_test():
    return render_template('socketio-test.html')


@socketio.on('reports add')
def reports_add(report):
    if validate_report(report):
        return abort(400)
    # TODO: Save report to database
    return jsonify(report=json_report(report))


@socketio.on('reports list')
def reports_list():
    # TODO: Load reports
    reports = []
    return jsonify(reports=[json_report(report) for report in reports])


@socketio.on('reports accept')
def reports_accept(report):
    if validate_report(report):
        return abort(400)
    # TODO: Load report from database and set it to accepted
    return jsonify(report=json_report(report))


@socketio.on('reports done')
def reports_accept(report):
    if validate_report(report):
        return abort(400)
    # TODO: Load report from database and set it to done
    return jsonify(report=json_report(report))

if __name__ == '__main__':
    socketio.run(app)
