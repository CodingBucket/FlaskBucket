from flask import render_template, redirect, request, url_for
from main import app, db
from models import Comment


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