from flask import render_template, request, redirect, url_for, abort
from . import main
from .. import db, photos
from flask_login import login_required, current_user
from ..models import User
from .forms import UpdateProfile 
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

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/post/<int:id>')
def post(id):

    '''
    View movie page function that returns the post details page and its data
    '''
    posts = Post.query.filter_by(id=id)
    comments = Comment.query.filter_by(post_id=id).all()

    return render_template('post.html',posts = posts,comments = comments)

@main.route('/post/new', methods = ['GET','POST'])
@login_required
def new_post():

    form = PostForm()
    my_stars = Star.query.filter_by(post_id=Post.id)

    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        user_p = current_user
        users = User.query.all()
        new_post = Post(user_p=current_user._get_current_object().id, title=title, description = description)
        for user in users:
            mail_message("New post","email/new_post",user.email,user=users)

        new_post.save_post()
        posts = Post.query.order_by(Post.posted_p.desc()).all()
        return render_template('posts.html', posts=posts)
    return render_template('new_post.html', form=form)