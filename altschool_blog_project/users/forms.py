import email
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from altschool_blog_project.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if user:

            raise ValidationError('The Username is already taken')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()

        if user:

            raise ValidationError('The email is already in use')



class LoginForm(FlaskForm):

    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember =BooleanField('Remember Me')
    submit = SubmitField('Log In')


class UpdateProfileForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpeg','png','jpg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if current_user.username != username.data :
            user = User.query.filter_by(username=username.data).first()

            if user:

                raise ValidationError('The Username is already taken')

    def validate_email(self, email):
        if current_user.email != email.data :
            user = User.query.filter_by(email = email.data).first()

            if user:

                raise ValidationError('The email is already in use')

class ResetRequestForm(FlaskForm):

    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        
        user = User.query.filter_by(email = email.data).first()

        if user is None:

            raise ValidationError('The Email Does Not Exist, Create A New Account')

class ResetPasswordForm(FlaskForm):

    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

