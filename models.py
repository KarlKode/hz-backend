from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creation_time = db.Column(db.DateTime)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'))
    type = db.Column(db.String(10))
    data = db.Column(db.String(100))

    def __init__(self, type, report=None, data=None):
        self.creation_time = datetime.now()
        self.type = type
        self.report = report
        self.data = data

    def __repr__(self):
        return '<Action %r, %r>' % (self.type, self.report)


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creation_time = db.Column(db.DateTime)
    name = db.Column(db.String(100))
    source = db.Column(db.String(10))
    number = db.Column(db.String(20))
    status = db.Column(db.String(15))
    lng = db.Column(db.Float)
    lat = db.Column(db.Float)
    needs = db.Column(db.String(100))
    needs_status = db.Column(db.String(15))
    skills = db.Column(db.String(100))
    photos = db.relationship('Photo', backref=db.backref('person', lazy='joined'), lazy='dynamic')
    actions = db.relationship('Action', backref=db.backref('person', lazy='joined'), lazy='dynamic')

    def __init__(self, name, source, status, lng, lat, needs, needs_status, skills, number=None):
        self.creation_time = datetime.now()
        self.name = name
        self.source = source
        self.number = number
        self.status = status
        self.lng = lng
        self.lat = lat
        if needs is not None:
            self.needs = ','.join(needs)
        else:
            self.needs = None
        self.needs_status = needs_status
        if needs is not None:
            self.skills = ','.join(skills)
        else:
            self.skills = ''
        print(needs)
        print(self.needs)
        print(skills)
        print(self.skills)

    def __repr__(self):
        return '<Report %r>' % self.id

    def to_dict(self):
        return {
            'id': self.id,
            'creation_time': repr(self.creation_time),
            'name': self.name,
            'source': self.source,
            'number': self.number,
            'status': self.status,
            'location': {'lat': self.lat, 'lng': self.lng},
            'needs': self.needs.split(',') if self.needs is not None else [],
            'needs_status': self.needs_status,
            'skills': self.skills.split(',') if self.skills is not None else [],
            'photos': [photo.data.decode('utf8') for photo in self.photos.all()],
            'actions': [action.type for action in self.actions.all()],
        }


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'))
    data = db.Column(db.BLOB)

    def __init__(self, report, data):
        self.report = report
        self.data = data

    def __repr__(self):
        return '<Photo %r>' % self.id
