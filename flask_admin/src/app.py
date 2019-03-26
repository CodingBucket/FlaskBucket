from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)

app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

admin = Admin(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))

admin.add_view(ModelView(Person, db.session))

if __name__ == '__main__':
    app.run()