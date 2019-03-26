from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.init_app(app)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    comment_text = db.Column(db.String(1000))

@app.route('/')
def index():
    comments = Comment.query.all()
    return render_template('index.html', comments=comments)

@app.route('/sign')
def sign():
    return render_template('sign.html')

@app.route('/sign', methods=['POST'])
def sign_post():
    name = request.form.get('name')
    comment = request.form.get('comment')

    new_comment = Comment(name=name, comment_text=comment)
    db.session.add(new_comment)
    db.session.commit()
    
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.secret_key = '123'
    app.run(debug=True)