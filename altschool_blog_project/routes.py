import email
from email import message
from fileinput import filename
from turtle import title
from altschool_blog_project import app, db, bcrypt, mail
from flask import render_template, request, redirect, url_for, flash,abort
from altschool_blog_project.forms import RegistrationForm, LoginForm, UpdateProfileForm, PostForm, ContactForm
from altschool_blog_project.models import User,Post,Message
from flask_login import login_user, current_user, logout_user, login_required
import secrets, os
from PIL import Image







@app.route('/')
def home():

    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page, per_page = 5)

    return render_template('home.html', posts = posts)

@app.route('/about')
def about():

    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()

    if form.validate_on_submit():
        
        
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        name = form.username.data
        email = form.email.data
        user = User(username = name, email = email, password = hashed_password)

        db.session.add(user)
        db.session.commit()
        flash(f' Account Created For {form.username.data}! You can now Log In', 'success')
        return redirect(url_for('login'))


    return render_template('register.html', title = 'Register', form = form)

@app.route('/login', methods= ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(email = form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):

            login_user(user, remember=form.remember.data)

            next_page = request.args.get('next')

            

            return redirect(next_page ) if next_page else redirect(url_for('home'))    

        else:
            flash('Log In failed, Use The Right Credentials', 'danger')


    return render_template('login.html', title='Login', form = form)

@app.route('/logout')
def logout():

    logout_user()

    return redirect(url_for('home'))

def save_picture(form_picture):

    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)

    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    # form_picture.save(picture_path)

    return picture_fn


@app.route('/profile', methods = ['GET', 'POST'])
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

        return redirect(url_for('profile'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email


    image_file = url_for('static', filename = 'profile_pics/'+current_user.image_file)
    return render_template('profile.html', title = 'Profile', image_file = image_file, form = form)

@app.route('/posts/new', methods=['GET', 'POST'])
@login_required
def create_post():

    form = PostForm()
    if form.validate_on_submit():

        title = form.title.data
        content = form.content.data
        post = Post(title = title, content= content, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post Has Been Created', 'success')

        return redirect(url_for('home'))
    return render_template('create_post.html', title='Create Post', form = form)

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    
    post = Post.query.get_or_404(post_id)

    return render_template('post.html', title= post.title, post = post, legend = 'New Post' )

@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    
    post = Post.query.get_or_404(post_id)
    
    if post.author != current_user:
        abort(403)
    
   
    form = PostForm()

    if form.validate_on_submit():
        
        post.title = form.title.data
        post.content = form.content.data

        db.session.commit()

        flash('Your Post Has been Updated', 'success')

        return redirect(url_for('post', post_id = post.id))

    elif request.method == 'GET':

        form.title.data = post.title
        form.content.data = post.content

    return render_template('create_post.html', title= post.title, form = form, legend = 'Update Post' )


@app.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    
    post = Post.query.get_or_404(post_id)
    
    if post.author != current_user:
        abort(403)
    
    else:
        db.session.delete(post)
        db.session.commit()

        flash('Your Post Has been Deleted', 'success')

        return redirect(url_for('home'))


@app.route('/user/<int:user_id>/posts', methods=['GET', 'POST'])
@login_required
def get_user_posts(user_id):
    
    page = request.args.get('page', 1, type=int)
    author = User.query.get_or_404(user_id)
    
    posts = Post.query.filter_by(author = author).order_by(Post.date_posted.desc()).paginate(page=page, per_page = 5)

    return render_template('user_posts.html', title = author.username, author = author, posts = posts)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if form.validate_on_submit():

        name = form.name.data
        email = form.email.data
        message = form.email.data

        contact_message = Message(name = name, email = email, message = message)

        db.session.add(contact_message)
        db.session.commit()

        flash('Your Message has Been Sent, we will get back to you soon!!', 'success')

        return redirect(url_for('home'))

        

    return render_template('contact.html', form = form, title = 'Contact')

