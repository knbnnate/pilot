from flask import Flask, render_template, request, url_for
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask_login import current_user
import os
import yaml
import json

# Create app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'not-so-super-secret'
# import .py object data from config directory
app.config.from_object('config.email')
app.config.from_object('config.security')
app.config.from_object('config.db')
mail = Mail(app)

# Create database connection object
db = SQLAlchemy(app)

# Define models
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(80), unique=True)
  description = db.Column(db.String(255))

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(255), unique=True)
  password = db.Column(db.String(255))
  active = db.Column(db.Boolean())
  confirmed_at = db.Column(db.DateTime())
  roles = db.relationship('Role', secondary=roles_users,
                          backref=db.backref('users', lazy='dynamic'))

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
# security instance should include passlib CryptContext that uses a good salty hash if you chose one in config.security
security = Security(app, user_datastore)

# Create a user to test with
@app.before_first_request
def create_db():
  db.create_all()
  db.session.commit()

# Views
@app.route('/')
@login_required
def home():
    return render_template('index.html')

@app.route('/game/<game>', methods = ['GET','POST','DELETE'])
def game(game):
  if request.method == 'GET':
    if os.path.isfile('var/game/{0}.yaml'.format(game)):
      stream = open('var/game/{0}.yaml'.format(game),'r')
      data = stream.read()
      stream.close()
      return render_template('get_data.html',data=yaml.safe_dump(yaml.safe_load(data),default_flow_style=False))
    else:
      return render_template('get_data.html',data=None)
  elif request.method == 'POST':
    data = request.get_json(force=True)
    stream = open('var/game/{0}.yaml'.format(game),'w')
    yaml.safe_dump(data, stream)
    stream.close()
    return render_template('get_data.html',data=yaml.safe_dump(data,default_flow_style=False))
  elif request.method == 'DELETE':
    pass

if __name__ == '__main__':
     app.run()
