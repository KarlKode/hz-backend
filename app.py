import random

from flask import Flask, render_template
from flask import request
from flask_socketio import SocketIO, emit
from twilio import twiml
from twilio.rest import TwilioRestClient

import settings
from models import db, Report, Photo, Action
from reports import validate_report, notify_report

app = Flask(__name__)
app.config.from_object(settings)
socketio = SocketIO(app)
db.init_app(app)

twilio = TwilioRestClient(app.config.get('TWILIO_SID'), app.config.get('TWILIO_TOKEN'))


def send_sms(number, message):
    return twilio.messages.create(
        to=number,
        from_=app.config.get('TWILIO_SMS_NUMBER'),
        body=message
    )


@app.route('/')
def overview():
    reports = Report.query.order_by(Report.id.desc()).all()
    return render_template('overview.html', reports=reports)


@app.route('/map')
def detail_map():
    reports = Report.query.order_by(Report.id.desc()).all()
    return render_template('detail_map.html', reports=reports)


@app.route('/logs')
def logs():
    reports = Report.query.order_by(Report.id.desc()).all()
    return render_template('logs.html', reports=reports)


@app.route('/actions')
def actions():
    return render_template('actions.html')


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
    lat_min = app.config.get('LOCATION_BOUNDS_LAT_MIN', 47.386)
    lat_max = app.config.get('LOCATION_BOUNDS_LAT_MAX', 47.393)
    lon_min = app.config.get('LOCATION_BOUNDS_LON_MIN', 8.505)
    lon_max = app.config.get('LOCATION_BOUNDS_LON_MAX', 8.525)
    for i in range(0, app.config.get('FAKE_DATA_POINTS', 10)):
        name = random.choice(('Marc', 'Dylan', 'Leo', 'Enes', 'Anna', 'Lea', 'Kurt', 'Chad', 'Lisa', 'Petra')) + ' '
        name += random.choice(('Gähwiler', 'Marriott', 'Helminger', '', 'Foobar', 'van Räudig', 'Kurz', 'Lang', 'On',
                               'Da'))
        source = random.choice(('ios', 'sms'))
        if source == 'sms':
            number = '+41798287644'
        else:
            number = None
        status = random.choice(('ok', 'injured', 'heavily_injured'))
        lat = random.uniform(lat_min, lat_max)
        lon = random.uniform(lon_min, lon_max)
        if status == 'ok':
            needs = random.choice(([], [], [], [], ['medic'], ['medic'], ['shelter'],
                                   ['medic', 'shelter', 'water'], ['shelter'], ['water'], ['food']))
        elif status == 'heavily_injured':
                needs = ['medic'] + random.choice(([], [], [], ['shelter'], ['shelter', 'water'], ['water'],
                                                   ['water', 'food'], ['food']))
        else:
            needs = random.choice(([], [], [], ['medic'], ['medic'], ['medic', 'shelter'],
                                   ['medic', 'shelter', 'water'], ['shelter'], ['water'], ['water', 'food'], ['food']))
        if needs:
            needs_status = random.choice(('open', 'open', 'open', 'open', 'open', 'processing', 'processing', 'done'))
        else:
            needs_status = 'done'
        if status == 'ok':
            skills = random.choice(([], [], [], [], [], ['medic'], ['medic'], ['medic'], ['medic', 'water'], ['water'],
                                    ['water', 'food'], ['food']))
        else:
            skills = []
        report = Report(name, source, status, lon, lat, needs, needs_status, skills, number)
        db.session.add(report)
    db.session.commit()
    return 'done'


@app.route('/twilio-sms', methods=['POST'])
def twilio_sms():
    number = request.form.get('From')
    message = request.form.get('Body')
    notify = False

    report = Report.query.filter_by(source='sms', number=number).first()
    if not report:
        report = Report(None, 'sms', None, None, None, None, None, None, number)
        db.session.add(report)
        response_msg = "Enter your full name."
    elif message.lower() == "delete":
        db.session.delete(report)
        response_msg = "Deleted your report."
    elif not report.name:
        report.name = message
        response_msg = "What's your status? Respond with \"ok\", \"injured\" or \"heavily injured\"."
    elif not report.status:
        response_msg = "What's your address? Respond with a sane address."
        message = message.lower()
        if message == "ok":
            report.status = 'ok'
        elif message == "injured":
            report.status = 'injured'
        elif message == "heavily injured":
            report.status = 'heavily_injured'
        else:
            response_msg = "Invalid response. What's your status? Respond with \"ok\", \"injured\" or " \
                           "\"heavily injured\"."
    elif report.lng is None:
        # TODO: Use google to get coordinates from address
        location = {'lng': 19, 'lat': 1}
        if location:
            report.lng = location['lng']
            report.lat = location['lat']
            response_msg = "Do you need help? Respond with \"none\", \"medical assistance\", \"shelter\", \"food\" or" \
                           " \"water\"."
        else:
            response_msg = "Invalid response. What's your address? Respond with a sane address."
    elif report.needs is None:
        if report.status == 'ok':
            response_msg = "Can you provide any help? Respond with \"none\", \"medical assistance\", \"food\" or " \
                           "\"water\"."
        else:
            response_msg = "Thank you for your information."
            report.skills = ''
            notify = True
        message = message.lower()
        if message == "none":
            report.needs = ''
            report.needs_status = 'done'
        else:
            report.needs_status = 'open'
            if message == "medical assistance":
                report.needs = 'medic'
            elif message == "shelter":
                report.needs = 'shelter'
            elif message == "food":
                report.needs = 'food'
            elif message == "water":
                report.needs = 'water'
            else:
                report.skills = None
                response_msg = "Invalid response. Do you need help? Respond with \"none\", \"medical assistance\", " \
                               "\"shelter\", \"food\" or \"water\"."
                notify = False
    elif report.skills is None:
        response_msg = "Thank you for your information."
        message = message.lower()
        notify = bool(report.needs)
        if message == "none":
            report.skills = ''
        elif message == "medical assistance":
            report.skills = 'medic'
        elif message == "food":
            report.skills = 'food'
        elif message == "water":
            report.skills = 'water'
        else:
            response_msg = "Invalid response. Can you provide any help? Respond with \"none\", \"medical assistance\"" \
                           ", \"food\" or \"water\"."
            notify = False
    else:
        # TODO: Check if somebody nearby needs assistance
        response_msg = "Unknown state!"

    if notify:
        notify_report(report)

    db.session.commit()
    return '''<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Message>%s</Message>
    </Response>''' % response_msg


@app.route('/tropo/debug', methods=['GET', 'POST'])
def tropo_debug():
    print(request.form)
    return 'done'


@app.route('/tropo', methods=['GET', 'POST'])
def tropo():
    status = request.form.get('status', None)
    needs = request.form.get('needs', None)
    skills = request.form.get('skills', None)
    lat_min = app.config.get('LOCATION_BOUNDS_LAT_MIN', 47.386)
    lat_max = app.config.get('LOCATION_BOUNDS_LAT_MAX', 47.393)
    lon_min = app.config.get('LOCATION_BOUNDS_LON_MIN', 8.505)
    lon_max = app.config.get('LOCATION_BOUNDS_LON_MAX', 8.525)
    lat = random.uniform(lat_min, lat_max)
    lon = random.uniform(lon_min, lon_max)
    if status is None or needs is None or skills is None:
        return 'error'
    report = Report("Anonymous", 'phone', status, lon, lat, [needs] if needs else [], 'open',
                    [skills] if skills else [], '+41798287644')
    db.session.add(report)
    db.session.commit()
    return 'done'


@socketio.on('reports add')
def reports_add(report_obj):
    if not validate_report(report_obj):
        return None
    location = report_obj.get('location', {'lat': None, 'lng': None})
    report = Report(report_obj.get('name'), 'ios', report_obj.get('status'), location.get('lng'), location.get('lat'),
                    report_obj.get('needs', []), report_obj.get('needs_status'), report_obj.get('skills', []))
    db.session.add(report)
    for photo_obj in report_obj.get('photos', []):
        photo = Photo(report, photo_obj.encode('utf8'))
        db.session.add(photo)
    action = Action('reports_add', report=report)
    db.session.add(action)
    db.session.commit()
    notify_report(report)
    if not report.skills:
        send_sms('+41798287644', "Your assistance is needed at " + str(report.lat) + " / " + str(report.lng) + "!")
    return report.to_dict()


@socketio.on('reports list')
def reports_list(foo):
    reports = Report.query.order_by(Report.creation_time.desc()).all()
    return [report.to_dict() for report in reports]


@socketio.on('reports accept')
def reports_accept(report_obj):
    report = Report.query.filter_by(id=report_obj.get('id', 0)).first_or_404()
    report.needs_status = 'processing'
    action = Action('reports_accept', report=report)
    db.session.add(action)
    db.session.commit()
    if True:
        send_sms('+41798287644', "Help is on the way!")
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
