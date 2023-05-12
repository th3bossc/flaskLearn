from flask import Blueprint, request, render_template
from flaskLearn.models import Post

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', default = 1, type = int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page, per_page = 12)
    return render_template('home.html', posts = posts, active = 'home')

@main.route('/about')
def about():
    return render_template('about.html', title = 'About', active = 'about')