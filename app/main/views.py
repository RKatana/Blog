from flask import render_template, request, redirect, url_for, abort
from . import main
from .. import db
from flask_login import login_required, current_user
from ..models import User
# from .forms import UpdateProfile, PostForm, CommentForm
# import markdown2

@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Welcome to Quote-flow'
    return render_template('index.html', title = title)
    
@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    title = 'Welcome to Quote-flow'
    return render_template("profile/profile.html", user = user, title=title)