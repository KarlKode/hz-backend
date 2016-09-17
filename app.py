from flask import Flask, render_template
from flask import request
from flask_socketio import SocketIO, emit

import settings
from models import db, Report, Photo, Action
from reports import validate_report

app = Flask(__name__)
app.config.from_object(settings)
socketio = SocketIO(app)
db.init_app(app)


@app.route('/')
def overview():
    return render_template('logs.html')


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


@app.route('/twilio-sms', methods=['POST'])
def twilio():
    number = request.form.get('From')
    message = request.form.get('Body')
    print('Got SMS from %r with text %r' % (number, message))

    response = 'Yeah this stuff really works: ' + message

    return '''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>%s</Message>
</Response>''' % response


@socketio.on('reports add')
def reports_add(report_obj):
    if not validate_report(report_obj):
        return None
    location = report_obj.get('location', {'lat': None, 'lng': None})
    report = Report(report_obj.get('name'), 'ios', report_obj.get('status'), location.get('lat'), location.get('lng'),
                    report_obj.get('needs', []), report_obj.get('needs_status'), report_obj.get('skills', []))
    db.session.add(report)
    for photo_obj in report_obj.get('photos', []):
        photo = Photo(report, photo_obj.encode('utf8'))
        db.session.add(photo)
    action = Action('reports_add', report=report)
    db.session.add(action)
    db.session.commit()
    emit('reports new', report.to_dict())
    # TODO: Notify all clients that could help that a new report has been added


@socketio.on('reports list')
def reports_list():
    reports = Report.query.order_by('creation_date').all()
    return [report.to_dict() for report in reports]


@socketio.on('reports accept')
def reports_accept(report_obj):
    if validate_report(report_obj):
        return None
    report = Report.query.filter_by(id=report_obj.id).first_or_404()
    report.needs_status = 'processing'
    action = Action('reports_accept', report=report)
    db.session.add(action)
    db.session.commit()
    return report.to_dict()


@socketio.on('reports done')
def reports_done(report_obj):
    if validate_report(report_obj):
        return None
    report = Report.query.filter_by(id=report_obj.id).first_or_404()
    report.needs_status = 'done'
    action = Action('reports_done', report=report)
    db.session.add(action)
    db.session.commit()
    return report.to_dict()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001)
