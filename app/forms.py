from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message='Email is Required')])
    password = PasswordField('Password', validators=[DataRequired(message='Password is Required')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message='Email is Required')])
    name = StringField('Name', validators=[DataRequired(message='Name is Required')])
    password = PasswordField('Password', validators=[DataRequired(message='Password Required')])
    password2 = PasswordField( 'Repeat Password', validators=[DataRequired(message='You Must Type Your Password Twice'), EqualTo('password', message='Passwords Must be the Same')])
    submit = SubmitField('Sign Up')


class BlogEditForm(FlaskForm):
    blogid = SelectField('Select Blog ID', validators=[DataRequired(message='Must Select a Blog')])
    blogabstract =  TextAreaField('Abstract', validators=[DataRequired(message='Abstract is Required')])
    blogbody = TextAreaField('Body', validators=[DataRequired(message='Blog Body is Required')])
    submit = SubmitField('Blog to Edit')