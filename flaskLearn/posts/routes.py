from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, abort
from flaskLearn.posts.forms import PostForm
from flaskLearn.models import Post
from flask_login import current_user, login_required
from flaskLearn import db

posts = Blueprint('posts', __name__)

@posts.route('/post/new', methods = ['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        flash('Post Successfully created', category = "success")
        post = Post(title = form.title.data, content = form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title = "New Post", form = form, legend = "Edit Post")



@posts.route("/post/<int:post_id>")
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id) #if id doesn't exist, gives a 404 not found
    return render_template('post.html', title = post.title, post = post)


@posts.route('/post/<int:post_id>/update', methods = ['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit() 
        flash("Post has been successfully edited", category = "success")
        return redirect(url_for('posts.post', post_id = post_id))
    elif request.method == 'GET':
        form.title.data = post.title 
        form.content.data = post.content
    return render_template('create_post.html', title = 'Edit Post', post = post, form = form, legend = "Edit Post")


@posts.route('/post/<int:post_id>/delete', methods = ['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()

    flash(message = "Post has been successfully deleted", category = 'success')
    return redirect(url_for('main.home'))