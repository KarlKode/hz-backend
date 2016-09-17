from flask import Flask, render_template, jsonify, abort
from flask_socketio import SocketIO, emit

import settings
from models import db, Report, Photo, Action
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


@socketio.on('my event')
def socketio_test_event(data):
    emit('my response', data)


@socketio.on('reports reset')
@app.route('/reset')
def reset():
    db.drop_all()
    db.create_all()
    # TODO: Insert dummy data
    return 'done'


@socketio.on('reports add')
def reports_add(report_obj):
    if validate_report(report_obj):
        return abort(400)
    report = Report(report_obj.name, 'ios', report_obj.status, report_obj.location.lng, report_obj.location.lng,
                    ','.join(report_obj.needs), report_obj.needs_status, ','.join(report_obj.skills))
    db.session.add(report)
    for photo_obj in report_obj.photos:
        photo = Photo(photo_obj)
        db.session.add(photo_obj)
        report.photos.add(photo)
    action = Action('reports_add', report=report)
    db.session.add(action)
    db.session.commit()
    return jsonify(report=json_report(report))


@socketio.on('reports list')
def reports_list():
    reports = Report.query.order_by('creation_date').all()
    return jsonify(reports=[json_report(report) for report in reports])


@socketio.on('reports accept')
def reports_accept(report_obj):
    if validate_report(report_obj):
        return abort(400)
    report = Report.query.filter_by(id=report_obj.id).first_or_404()
    report.needs_status = 'processing'
    action = Action('reports_accept', report=report)
    db.session.add(action)
    db.session.commit()
    return jsonify(report=json_report(report_obj))


@socketio.on('reports done')
def reports_done(report_obj):
    if validate_report(report_obj):
        return abort(400)
    report = Report.query.filter_by(id=report_obj.id).first_or_404()
    report.needs_status = 'done'
    action = Action('reports_done', report=report)
    db.session.add(action)
    db.session.commit()
    return jsonify(report=json_report(report_obj))

if __name__ == '__main__':
    socketio.run(app)
