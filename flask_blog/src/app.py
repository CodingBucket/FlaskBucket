from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)

@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.filter_by(id=post_id).one()
    date_posted = post.date_posted.strftime('%B %d, %Y')
    return render_template('post.html', post=post, date_posted=date_posted)

@app.route('/add_post')
def add_post():
    return render_template('post/add_post.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/addpost', methods=['POST'])
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']
    date_posted = datetime.now()

    new_post = Post(
        title=title, 
        subtitle=subtitle, 
        author=author, 
        content=content, 
        date_posted=date_posted
    )
    db.session.add(new_post)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()