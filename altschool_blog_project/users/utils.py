import secrets, os
from PIL import Image
from flask_mail import Message
from flask import url_for, current_app
from altschool_blog_project import mail

def save_picture(form_picture):

    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)

    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    # form_picture.save(picture_path)

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender = 'temitopeadebayo749@gmail.com', recipients=[user.email])
    msg.body = f"""
        To reset Your password, visit the following link
        {url_for('users.reset_password', token= token, _external = True)}

        If you did not send this request simply ignore this mail
    """
    mail.send(msg)
