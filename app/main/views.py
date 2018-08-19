
from flask import flash, render_template, request, current_app
from flask import session, redirect, url_for
from forms import CommentForm, EditProfileForm, NameForm, PostForm
from blueprint import main
from flask_login import login_required, current_user


@main.route('/debug', methods=['GET', 'POST'])
def debug():
    from entity import Post, User
    from flasky import db
    from werkzeug.security import generate_password_hash

    old = 'q'
    new = '1234'

    user = User.query.offset(0).first()
    names = [ follow.follower_id for follow in user.followers]

    return str(user.username) + str(names) + str(user.followers.count())

@main.route('/init_data')
def init_data():
    from fake import users, posts, comments, follows
    from flasky import db
    db.drop_all()
    db.create_all()
    users()
    posts()
    comments()
    # follows()
    return 'data init successfully'

@main.route('/follow', methods=['POST'])
@login_required
def follow():
    from entity import Post, User
    from flasky import db
    followed_id = request.form.get('followed_id', None)
    followed = User.query.filter_by(id=followed_id).first()
    current_user.follow(followed)
    db.session.commit()
    flash(  'follow successfully.')
    return ''

@main.route('/unfollow', methods=['POST'])
@login_required
def unfollow():
    from entity import Post, User
    from flasky import db
    followed_id = request.form.get('followed_id', None)
    followed = User.query.filter_by(id=followed_id).first()
    current_user.unfollow(followed)
    db.session.commit()
    flash(  'follow successfully.')
    return ''


@main.route('/', methods=['GET', 'POST'])
def index():
    from entity import Post

    form = PostForm()
    if form.validate_on_submit():
        write_post(form)
        return redirect(url_for('.index'))

    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['INDEXPOST_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()) \
        .paginate(page, per_page=per_page, error_out=False)
    return render_template('index.html', form=form, pagination=pagination)

def write_post(form):
    from entity import Post
    from flasky import db
    post = Post(title=form.title.data,
                body=form.body.data,
                author=current_user._get_current_object())
    db.session.add(post)
    db.session.commit()

@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    from entity import Post, User


    form = EditProfileForm()
    if form.validate_on_submit():
        from flasky import db
        profile = {
            'name': form.name.data,
            'location': form.location.data,
            'about_me': form.about_me.data,
        }
        User.query.filter_by(username=current_user.username).update(profile)
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/user/<username>')
def user(username):
    from entity import Post, User
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['USERPOST_PER_PAGE']
    pagination = user.posts.order_by(Post.timestamp.desc())\
        .paginate(page, per_page=per_page, error_out=False)
    return render_template('user.html', user=user, pagination=pagination)


@main.route('/post', methods=['GET', 'POST'])
@main.route('/post/<post_id>', methods=['GET', 'POST'])
def post(post_id):
    from entity import Post, Comment
    post = Post.query.filter_by(id=post_id).first()
    form = CommentForm()

    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.timestamp)
    comment_count = current_app.config['FLASKY_COMMENTS_PER_PAGE']
    page = request.args.get('page', 1, type=int)
    pagination = comments.paginate(page, error_out=False, per_page=comment_count)
    return render_template('post.html', post=post, form=form,
        pagination=pagination)

@main.route('/comment', methods=['GET', 'POST'])
def comment():
    form = CommentForm()
    submit_comment(form)
    return ''

def submit_comment(form):
    from flasky import db
    from entity import Post, Comment, User

    post_id = request.args.get('post_id', None)
    target_id = request.args.get('target_id', None)
    post = Post.query.filter_by(id=post_id).first()
    target = User.query.filter_by(id=target_id).first()
    comment = Comment(body=form.content.data,
                      post=post,
                      author=current_user,
                      target=target)
    db.session.add(comment)
    db.session.commit()
    flash('comment successfully.')


@main.route('/index')
def index1():
    return 'index'

@main.route('/static/source')
def get_source(source):
    return source
