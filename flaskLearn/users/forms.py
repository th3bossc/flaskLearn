from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskLearn.models import User



class RegistrationForm(FlaskForm):
    username = StringField(
        'Username', 
        validators = [DataRequired(), Length(min = 2, max = 20)],
    )
    email = StringField(
        'Emaill',
        validators = [DataRequired(), Email()]
    )

    password = PasswordField(
        'Password',
        validators = [DataRequired(), Length(min = 8)]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators = [DataRequired(), EqualTo('password')]
    )

    submit = SubmitField('Sign up')


    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one')
        
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('Email already exists. Please Log in via link below')



class LoginForm(FlaskForm):
    email = StringField(
        'Emaill',
        validators = [DataRequired(), Email()]
    )

    password = PasswordField(
        'Password',
        validators = [DataRequired(), Length(min = 8)]
    )
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')



class UpdateProfileForm(FlaskForm):
    username = StringField(
        'Username', 
        validators = [DataRequired(), Length(min = 2, max = 20)],
    )
    email = StringField(
        'Email',
        validators = [DataRequired(), Email()]
    )

    picture = FileField(
        'Update Profile Pic', 
        validators = [FileAllowed(['jpg', 'png', 'gif'])]
    )

    submit = SubmitField('Save Changes')


    def validate_username(self, username):
        if (username.data != current_user.username):
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError('Username already taken. Please choose a different one')
        
    def validate_email(self, email):
        if (email.data != current_user.email):
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('Email already exists. Please Log in via link below')
            

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    submit = SubmitField('Send Verification Code') 

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is None:
            raise ValidationError(message = "Email does not exist within our servers, Please create an account", category = "info")
        

class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        'Password',
        validators = [DataRequired(), Length(min = 8)]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators = [DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Confirm new password')