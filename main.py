from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Lindenwood09!@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

#built a table for my database
class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(120))
    blog_post = db.Column(db.Text())

    def __init__(self, blog_title, blog_post):
        self.blog_title = blog_title
        self.blog_post = blog_post

# route to /blog
@app.route('/blog', methods = ['POST','GET'])
def home():
    #table
    blog = Blog.query.all()
    return render_template('blog.html', title="Build a Blog", blog=blog)

#route to new blog post
@app.route('/new-post', methods=['POST', 'GET'])
def new_post():
    blog_title = ''
    blog_post = ''
    title_error = ''
    body_error = ''

#if statements over what gonna or not gonna be posted!
    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_post = request.form['blog_post']
        if blog_title == '':
            title_error = 'Title please and Thank You'
        elif blog_post == '':
            body_error = 'Your really gonna leave this blank... add something please'
        else:
            new_blog = Blog(blog_title, blog_post)
            db.session.add(new_blog)
            db.session.commit()
            
            return redirect('/single-post?id={0}'.format(new_blog.id))

    return render_template('newpost.html', title="New Post", title_error=title_error,
                body_error=body_error, blog_post=blog_post, blog_title=blog_title)

#routes the page to blog
@app.route('/', methods=['POST', 'GET'])
def index():
    return redirect ('/blog')

#routes to a single post
@app.route('/single-post', methods=['GET'])
def single_post():
    retrieved_id = request.args.get('id')
    blog = db.session.query(Blog.blog_title, Blog.blog_post).filter_by(id=retrieved_id)
    return render_template('single_blog.html', title="Single Post", blog=blog)

if __name__ == '__main__':
    app.run()