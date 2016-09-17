from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creation_time = db.Column(db.DateTime)
    type = db.Column(db.String(10))
    report = db.relationship('Report', backref='action', lazy='dynamic')

    def __init__(self, type, report):
        self.creation_time = datetime.now()
        self.type = type
        self.report = report

    def __repr__(self):
        return '<Action %r, %r>' % (self.type, self.report.id)


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    source = db.Column(db.String(10))
    number = db.Column(db.String(20))
    status = db.Column(db.String(15))
    lng = db.Column(db.Float)
    lat = db.Column(db.Float)
    needs = db.Column(db.String(100))
    needs_status = db.Column(db.String(15))
    skills = db.Column(db.String(100))
    photos = db.relationship('Photo', backref='report', lazy='dynamic')

    def __init__(self, name, source, status, lng, lat, needs, needs_status, skills, number=None):
        self.name = name
        self.source = source
        self.number = number
        self.status = status
        self.lng = lng
        self.lat = lat
        self.needs = ','.join(needs)
        self.needs_status = needs_status
        self.skills = ','.join(skills)

    def __repr__(self):
        return '<Report %r>' % self.id


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.BLOB)

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return '<Photo %r>' % self.id

"""name: "Max Muster",
  source: "ios|phone",
  number: "+41791231234", // can also be null
  status: "ok|injured|heavily_injured",
  location: {
    lat: 12.000,
    lng: 13.000
  },
  needs: ["medic", "food", "water"],
  needs_status: "open|processing|done",
  skills: ["medic", "food", "water"],
  photos: ["base64 of first photo", "base64 of second photo"]"""
