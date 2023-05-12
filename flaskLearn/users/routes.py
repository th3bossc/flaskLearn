from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
from flaskLearn.users.forms import RegistrationForm, LoginForm, UpdateProfileForm, RequestResetForm, ResetPasswordForm
from flaskLearn.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flaskLearn import db, bcrypt
from flaskLearn.users.  utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

@users.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(password = form.password.data).decode('utf-8')
        new_user = User(username = form.username.data, email = form.email.data, password = hashed_pwd)
        db.session.add(new_user)
        db.session.commit()
        flash(message = f'Account created for {form.username.data}!', category = "success")
        login_user(new_user)
        return redirect(url_for('users.profile'))
    return render_template('register.html', title = "Registration", form = form)

@users.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(pw_hash = user.password, password = form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page is not None else redirect(url_for('main.home'))
        flash(message = "Login unsuccessful. Please check username and password", category = "danger")         
    return render_template('login.html', title = "Login", form = form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data 
        db.session.commit() 
        flash(message = 'Account details have been updated', category = 'success')
        return redirect(url_for('users.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('profile.html', title = 'User Profile', image_file = image_file, form = form)


@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', default = 1, type = int)
    user = User.query.filter_by(username = username).first_or_404()
    posts = Post.query.filter_by(author = user).order_by(Post.date_posted.desc()).paginate(page = page, per_page = 5)
    return render_template('user_posts.html', posts = posts, user = user)


@users.route('/reset_password', methods = ['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash(message = "Email sent successfully! Please check your inbox", category = 'info') 
        return redirect((url_for('users.login')))
    return render_template('reset_request.html', title = 'Reset Password', form = form)

@users.route('/reset_password/<string:token>', methods = ['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    
    if user is None:
        print(token)
        flash(message = 'Token has been expired', category = 'warning')
        return redirect(url_for('users.reset_request')) 
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(password = form.password.data).decode('utf-8')
        user.password = hashed_pwd
        #db.session.add(new_user)
        db.session.commit()
        flash(message = 'Your password has been successfully updated. Kindly LogIn with new details', category = "success")
        return redirect(url_for('users.login'))
    return render_template('reset_password.html', title = "Reset Password", form = form)


