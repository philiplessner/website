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


class BlogSelectForm(FlaskForm):
    blogid = SelectField('Select Blog ID', validate_choice=False, coerce=int)
    submit_edit = SubmitField('Edit a Blog')
    submit_new = SubmitField('Create a New Blog Entry')


class BlogEditForm(FlaskForm):
    blogtitle = TextAreaField('Title', validators=[DataRequired(message='Title is Required')])
    blogabstract =  TextAreaField('Abstract', validators=[DataRequired(message='Abstract is Required')])
    blogbody = TextAreaField('Body', validators=[DataRequired(message='Blog Body is Required')])
    blogpagecss = TextAreaField('Custom CSS')
    blogdate = StringField('Date', validators=[DataRequired(message='Date is Required')])
    blogmedialink = StringField('Media Link', validators=[DataRequired(message='Link to Media is Required')])
    blogmediatype = StringField('Media Type', validators=[DataRequired(message='Media Type is Required')])
    submit_commit = SubmitField('Publish to Database')
    submit_cancel = SubmitField('Cancel', render_kw={'formnovalidate': True})