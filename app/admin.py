from datetime import date, datetime, timedelta, timezone

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.models import Blog, User

from . import db
from .forms import (
    AnalyticsDateRangeForm,
    BlogEditForm,
    BlogSelectForm,
    LoginForm,
    SignupForm,
)
from .graphs import (
    countryCodes_humans,
    countryCodes_robots,
    endpoints_humans,
    endpoints_robots,
    log_date_bounds,
    visits,
)

admin = Blueprint('admin', __name__)


def flash_form_errors(form):
    for field in form:
        for error in field.errors:
            flash(error)


@admin.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if (request.method == 'GET'):
        return render_template('login.html', form=form)
    user = None
    if form.validate_on_submit():
        stmt = db.select(User).where(User.email == form.email.data)
        user = db.session.scalars(stmt).first()
    else:  # Missing data
        flash_form_errors(form)
        return redirect(url_for('admin.login'))

    # Incorrect data
    if not user or not check_password_hash(user.password_hash, form.password.data):
        flash('Incorrect Email or Password. Please check your login details and try again.')
        return redirect(url_for('admin.login'))

    login_user(user, remember=form.remember_me.data)
    return redirect(url_for('admin.profile'))

@admin.route('/signup')
@login_required
def signup():
    form = SignupForm()
    if not current_user.is_authenticated:
        return redirect(url_for('admin.login'))
    return render_template('signup.html', form=form)

@admin.route('/signup', methods=['POST'])
def signup_post():
    form = SignupForm()
    user = None
    if form.validate_on_submit():
        stmt = db.select(User).where(User.email == form.email.data)
        user = db.session.scalars(stmt).first()
        if user: # User already exists
            flash('Email address already exists')
            return redirect(url_for('admin.signup'))
        else: # Success!
            new_user = User(email=form.email.data, name=form.name.data, password_hash=generate_password_hash(form.password.data))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('admin.login'))
    else:  # Data validation failed
        flash_form_errors(form)
        return redirect(url_for('admin.signup'))

@admin.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

@admin.route('/profile')
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for('admin.login'))
    return render_template('profile.html', current_user_name=current_user.name)

@admin.route('/blogselect', methods=['GET', 'POST'])
def blog_select():
    if not current_user.is_authenticated:
        return redirect(url_for('admin.login'))
    form = BlogSelectForm(request.form)
    if (request.method == 'GET'):
        stmt = (db.select(Blog.title, Blog.abstract, Blog.date, Blog.medialink, Blog.mediatype, Blog.id)
                        .select_from(Blog)
                        .order_by(Blog.date.desc()))
        blogs = db.session.execute(stmt).all()
        template_data = {'blogs': blogs}
        blog_ids = [t[5] for t in blogs]
        form.blogid.choices = blog_ids
        return render_template('blogselect.html', **template_data, form=form)
    if form.validate_on_submit():
        if form.submit_edit.data:  # If user clicked the edit button
            return redirect(url_for('admin.blog_edit', blogid=form.blogid.data))
        elif form.submit_new.data: # If user clicked the new button
            return redirect(url_for('admin.blog_edit', blogid=-1))
        elif form.submit_delete.data: # If user clicked on the delete button
            stmt = db.select(Blog).where(Blog.id == form.blogid.data)
            blog2delete = db.session.execute(stmt).scalar_one_or_none()
            db.session.delete(blog2delete)
            db.session.commit()
            return redirect(url_for('admin.blog_select'))

@admin.route('/blogedit/<blogid>', methods=['GET', 'POST'])
def blog_edit(blogid):
    if not current_user.is_authenticated:
        return redirect(url_for('admin.login'))
    form = BlogEditForm(request.form)
    if (int(blogid) >= 0): # Existing Blog
        stmt = db.select(Blog).where(Blog.id == blogid)
        blog = db.session.scalars(stmt).first()
    if (request.method == 'GET' and int(blogid) >= 0): # For GET request, populate the form with database records, if an existing blog
        form.blogtitle.data = blog.title
        form.blogdate.data = blog.date
        form.blogabstract.data = blog.abstract
        form.blogbody.data = blog.body
        form.blogmedialink.data = blog.medialink
        form.blogmediatype.data = blog.mediatype
        form.blogpagecss.data = None if blog.pagecss == '' else blog.pagecss
        return render_template('blogedit.html', form=form, blogid=blogid)
    elif (request.method == 'GET' and int(blogid) < 0): # For GET request, create am empty form, if new blog
        form.blogtitle.data = ''
        form.blogdate.data = ''
        form.blogabstract.data = ''
        form.blogbody.data = ''
        form.blogmedialink.data = ''
        form.blogmediatype.data = ''
        form.blogpagecss.data = ''
        return render_template('blogedit.html', form=form, blogid=blogid)
    if (request.method == 'POST'):  # For POST request, write new data to database using info. in form or Cancel
        if form.submit_cancel.name in request.form:
                return redirect(url_for('admin.blog_select'))
        if form.validate_on_submit(): 
            if form.submit_commit.data and int(blogid) >= 0: # Updating an existing blog entry
                blog.title = form.blogtitle.data
                blog.date = form.blogdate.data
                blog.abstract = form.blogabstract.data
                blog.body = form.blogbody.data
                blog.medialink = form.blogmedialink.data
                blog.mediatype = form.blogmediatype.data
                blog.pagecss = None if form.blogpagecss.data == '' else form.blogpagecss.data
                db.session.commit()
            elif form.submit_commit.data and int(blogid) < 0:
                blog_dict = {'title': form.blogtitle.data,
                             'date': form.blogdate.data,
                             'abstract': form.blogabstract.data,
                             'body': form.blogbody.data,
                             'medialink': form.blogmedialink.data,
                             'mediatype': form.blogmediatype.data,
                             'pagecss': None if form.blogpagecss.data == '' else form.blogpagecss.data}
                record = Blog(**blog_dict)
                db.session.add(record)
                db.session.commit()
            return redirect(url_for('admin.blog_select'))
        else: # Data Error in form
            flash_form_errors(form)
            return render_template('blogedit.html', form=form, blogid=blogid)


@admin.route('/analytics', methods=['GET', 'POST'])
def analytics():
    if not current_user.is_authenticated:
        return redirect(url_for('admin.login'))

    now = datetime.now(tz=timezone.utc)
    default_start_date = (now - timedelta(days=31)).date()
    default_end_date = (now - timedelta(days=1)).date()
    oldest_date_string, newest_date_string = log_date_bounds()
    form = AnalyticsDateRangeForm()
    date_error = None
    start_date = default_start_date
    end_date = default_end_date

    if oldest_date_string is None or newest_date_string is None:
        date_error = 'No dates are available in the analytics database.'
    else:
        oldest_date = date.fromisoformat(oldest_date_string)
        newest_date = date.fromisoformat(newest_date_string)

        if request.method == 'GET':
            form.start_date.data = default_start_date
            form.end_date.data = default_end_date
        elif form.validate_on_submit():
            if form.start_date.data > form.end_date.data:
                date_error = 'The start date must be on or before the end date.'
            elif form.start_date.data < oldest_date or form.end_date.data > newest_date:
                date_error = (
                    f'Dates must be between {oldest_date_string} and '
                    f'{newest_date_string}.'
                )
            else:
                start_date = form.start_date.data
                end_date = form.end_date.data
        else:
            date_error = 'Please select valid start and end dates.'

    start_time = f'{start_date.isoformat()} 00:00:00'
    end_time = f'{end_date.isoformat()} 23:59:59'
    countryCodes_humans_data = countryCodes_humans(start_time, end_time)
    countryCodes_robots_data = countryCodes_robots(start_time, end_time)
    endpoints_humans_data = endpoints_humans(start_time, end_time)
    endpoints_robots_data = endpoints_robots(start_time, end_time)
    visits_data = visits(start_time, end_time)
    templateData = {
        'country_chart_data_humans': countryCodes_humans_data,
        'endpoint_chart_data_humans': endpoints_humans_data,
        'country_chart_data_robots': countryCodes_robots_data,
        'endpoint_chart_data_robots': endpoints_robots_data,
        'visits_chart_data': visits_data,
        'date_form': form,
        'date_error': date_error,
        'oldest_date': oldest_date_string,
        'newest_date': newest_date_string,
    }
    return render_template('analytics.html', **templateData)
