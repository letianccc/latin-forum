from random import randint
import random
from sqlalchemy.exc import IntegrityError
from faker import Faker
from flasky import db
from entity import User, Post, Comment, Follow


def users(count=10):
    init_admin()
    fake = Faker()
    i = 0
    while i < count:
        u = User(email=fake.email(),
                 username=fake.user_name(),
                 password='password',
                 name=fake.name(),
                 location=fake.city(),
                 about_me=fake.text(),
                 regist_time=fake.past_date())

        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()

def init_admin():
    fake = Faker()
    u = User(email=fake.email(),
             username='t',
             password='123',
             name=fake.name(),
             location=fake.city(),
             about_me=fake.text(),
             regist_time=fake.past_date())
    db.session.add(u)
    db.session.commit()



def posts(count=20):
    fake = Faker()
    user_count = User.query.count()
    for i in range(user_count):
        user = User.query.offset(i).first()
        for j in range(count):
            p = Post(title=fake.text(),
                     body=fake.text(),
                     timestamp=fake.past_date(),
                     author=user)
            db.session.add(p)
    db.session.commit()

def comments(count=5):
    fake = Faker()
    user_count = User.query.count()

    post_count = Post.query.count()
    for i in range(post_count):
        post = Post.query.offset(i).first()

        for i in range(count):
            user = User.query.offset(randint(0, user_count - 1)).first()
            comment = Comment(body=fake.text(),
                     timestamp=fake.past_date(),
                     author=user,
                     post=post)
            db.session.add(comment)
    db.session.commit()

def follows(count=5):
    user_count = User.query.count()
    for i in range(user_count):
        user = User.query.offset(i).first()
        ids = random.sample(range(0, user_count), count)
        if user.id in ids:
            ids.remove(user.id)
        for id in ids:
            follower = User.query.offset(id).first()
            f = Follow(followed=user, follower=follower)
            db.session.add(f)
    db.session.commit()



if __name__ == '__main__':
    users()
    posts()
