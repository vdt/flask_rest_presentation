"""
This module contains all of the access to the
data methods (database access)
"""

import os

from application import app
from flask_sqlalchemy import SQLAlchemy


# create the database instance
basepath = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basepath, "presentation.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)


class Name(db.Model):
    '''
    This class encapsulates the names database
    '''
    lname = db.Column(db.String, primary_key=True)
    fname = db.Column(db.String)
    timestamp = db.Column(db.TIMESTAMP)

    def __init__(self, last_name, first_name, timestamp):
        self.lname = last_name
        self.fname = first_name
        self.timestamp = timestamp

    def __call__(self):
        # convert the data into a JSON serializeable dictionary
        return {
            "lname": self.lname,
            "fname": self.fname,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }


class Model(object):
    """
    This class defines the access to the application
    data
    """
    def get_names(self):
        return Name.query.all()

    def get_name(self, last_name):
        return Name.query.filter_by(lname=last_name).one()

    def create_name(self, last_name, first_name):
        name = Name(last_name, first_name, datetime.now())
        db.session.add(name)
        db.session.commit()
        return name

    def update_name(self, last_name, first_name=None):
        name = Name.query.filter_by(lname=last_name).one()
        name.lname = last_name
        name.fname = first_name if first_name is not None else name.fname
        db.session.add(name)
        db.session.commit()
        return name

    def delete_name(self, last_name):
        name = Name.query.filter_by(lname=last_name).one()
        db.session.delete(name)
        db.session.commit()



