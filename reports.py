import twilio
from flask.ext.socketio import emit

from models import Report


def validate_report(report_obj):
    # TODO
    return True


def notify_report(report):
    emit('reports new', report.to_dict())
