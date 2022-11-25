from flask import Blueprint, render_template, redirect, request, flash, url_for
from altschool_blog_project.main.forms import ContactForm
from altschool_blog_project.models import Post, Message
from altschool_blog_project import db


main = Blueprint('main', __name__)


@main.route('/')
def home():

    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page, per_page = 5)

    return render_template('home.html', posts = posts)

@main.route('/about')
def about():

    return render_template('about.html')



@main.route('/contact', methods=['GET', 'POST'])
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

        return redirect(url_for('main.home'))

        

    return render_template('contact.html', form = form, title = 'Contact')