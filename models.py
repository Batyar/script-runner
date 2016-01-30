from app import app
from flask import flash
from flask.ext.bcrypt import generate_password_hash
from flask.ext.sqlalchemy import SQLAlchemy
from os import listdir, makedirs
from os.path import isfile, join, exists
from subprocess import call

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:909090@localhost/wsr'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))
    role = db.Column(db.String(10))

    def __init__(self, name, password, role = 'user'):
        self.name = name
        self.password = generate_password_hash(password)
        self.role = role

    def __repr__(self):
        return '<User %r>' % self.name

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def run(self, script):
        try:
            path = self.name + '/' + script.name
            call(['chmod', '+x', path])
            call(['./' + path] + script.arguments.split())
        except OSError:
            return flash('Incorrect script name or arguments')

    def clear_scripts(self):
        directory = self.name
        if not exists(directory):
            makedirs(directory)
        arr = [ f for f in listdir(self.name) if isfile(join(self.name,f)) ]
        for script in self.scripts:
            if script.name not in arr:
                db.session.delete(script)


    @staticmethod
    def find_by_name(username):
        user = User.query.filter_by(name=username).first()
        return user

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

class Script(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    arguments = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='scripts', lazy='joined')

    def __init__(self, name, arguments, user):
        self.name = name
        self.arguments = arguments
        self.user = user

    def save(self):
        db.session.add(self)
        db.session.commit()
        self.create_data()
        return self

    def create_data(self):
        directory = self.user.name
        if not exists(directory):
            makedirs(directory)
        open(directory + '/%s' % self.name, 'w+')
        open(directory + '/%s.output' % self.name, 'w+')

    def check_arguments(self):
        result = [False for e in self.arguments if not e.isalnum() and e not in [' ', '-']]
        return False if False in result else True