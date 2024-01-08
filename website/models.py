from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func


#These blocks are like classes, Every created Note, User, etc  must conform to their parameters

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#If I wanted to add more funcionality I would need to add another class which would inherit from db.model then define all the fields I would want. I can look it up on Flask.sql.alchemy. Then add foreign key

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_Name = db.Column(db.String(150))
    notes = db.relationship('Note')