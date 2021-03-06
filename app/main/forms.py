
from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField
from wtforms.validators import Length, DataRequired
from flask_pagedown.fields import PageDownField


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = PageDownField("What's on your mind?", validators=[DataRequired()])
    submit = SubmitField('Submit')

class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    content = TextAreaField('comment')
    submit = SubmitField('submit')
