from flask import Blueprint, render_template, redirect, url_for, flash, request
from altschool_blog_project.users.forms import RegistrationForm, LoginForm, UpdateProfileForm, ResetPasswordForm, ResetRequestForm
from flask_login import current_user, login_user, logout_user, login_required
from altschool_blog_project import db, bcrypt
from altschool_blog_project.models import User, Post
from altschool_blog_project.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()

    if form.validate_on_submit():
        
        
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        name = form.username.data
        email = form.email.data
        user = User(username = name, email = email, password = hashed_password)

        db.session.add(user)
        db.session.commit()
        flash(f' Account Created For {form.username.data}! You can now Log In', 'success')
        return redirect(url_for('users.login'))


    return render_template('register.html', title = 'Register', form = form)

@users.route('/login', methods= ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(email = form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):

            login_user(user, remember=form.remember.data)

            next_page = request.args.get('next')

            

            return redirect(next_page ) if next_page else redirect(url_for('main.home'))    

        else:
            flash('Log In failed, Use The Right Credentials', 'danger')


    return render_template('login.html', title='Login', form = form)

@users.route('/logout')
def logout():

    logout_user()

    return redirect(url_for('main.home'))

@users.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()

    if form.validate_on_submit():

        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
 
        current_user.username = form.username.data
        current_user.email = form.email.data

        db.session.commit()

        flash('Your Profile has been Updated', 'success')

        return redirect(url_for('users.profile'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email


    image_file = url_for('static', filename = 'profile_pics/'+current_user.image_file)
    return render_template('profile.html', title = 'Profile', image_file = image_file, form = form)

@users.route('/user/<int:user_id>/posts', methods=['GET', 'POST'])
@login_required
def get_user_posts(user_id):
    
    page = request.args.get('page', 1, type=int)
    author = User.query.get_or_404(user_id)
    
    posts = Post.query.filter_by(author = author).order_by(Post.date_posted.desc()).paginate(page=page, per_page = 5)

    return render_template('user_posts.html', title = author.username, author = author, posts = posts)

@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = ResetRequestForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)

        flash('An Email Has Been Sent WIth Instructions on How To Change The Password', 'success')

        return redirect(url_for('users.login'))

    return render_template('reset_request.html', title = 'Reset Password', form = form)



@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.verify_reset_token(token)

    if user is None:
        flash('The Token Is Invalid or Expired', 'warning')
        return redirect(url_for('users.reset_request'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password


        db.session.commit()
        flash(f' Your Password has been changed. You can now Log In', 'success')
        return redirect(url_for('users.login'))

    return render_template('reset_password.html', title= "Reset PassWord", form = form)