from flask import session, render_template, flash, request, url_for, redirect
from . import auth
from forms import ChangePasswordForm, LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    from entity import User


    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    from entity import User
    from flasky import db
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    from flasky import db

    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.commit()

            logout_user()

            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form)
