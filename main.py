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

# route to blog
@app.route('/blog', methods = ['POST','GET'])
def home():
    view = 'default'
    blog = []
    # If this does have an id redirect this to single blog
    if request.args:
        #retrieved_id = request.args.get('id')
        id = request.args.get('id')
        blog.append(Blog.query.get(id))
        view = 'single'

    # If this has no id return to home blog page 
    else: 
        blog = Blog.query.all()

    return render_template('blog.html', title="Build a Blog", blog=blog, view=view)
        

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
        # title error message
        if blog_title == '':
            title_error = 'Title please and Thank You'
        # post error message
        elif blog_post == '':
            body_error = 'Your really gonna leave this blank... add something please'
        else:
            new_blog = Blog(blog_title, blog_post)
            db.session.add(new_blog)
            db.session.commit()
            retrieved_id = str(new_blog.id)
            return redirect('/blog?id=' + retrieved_id )

    return render_template('newpost.html', title="New Post", title_error=title_error,
                body_error=body_error, blog_post=blog_post, blog_title=blog_title)

#routes the page to blog
@app.route('/', methods=['POST', 'GET'])
def index():
    return redirect ('/blog')

if __name__ == '__main__':
    app.run()