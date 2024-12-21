from flask import Flask, render_template, request
from flask_cors import CORS

from blog_app.database import db, Post
from blog_app.posts import convert_posts_to_json, convert_post_to_json
from blog_app.config import Config

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return convert_posts_to_json(posts)


@app.route('/posts', methods=['POST'])
def create_post():
    data = request.json
    if 'content' not in data:
        return {'error': 'content is required'}, 400
    new_post = Post(content=data['content'])
    db.session.add(new_post)
    db.session.commit()
    return convert_post_to_json(new_post), 201


def run():
    app.run(debug=False, host=app.config['HOST'], port=app.config['PORT'])
