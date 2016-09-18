from flask_socketio import emit


def validate_report(report_obj):
    # TODO
    return True


def notify_report(report):
    emit('reports new', report.to_dict())
