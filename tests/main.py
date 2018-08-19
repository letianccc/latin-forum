import unittest
from flasky import create_app, db
from entity import User, Follow
from app.auth.forms import RegistrationForm
from flask import session, url_for
import re
from datetime import datetime

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        app = create_app('testing')
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self, username, password):
        data = {
            'username': username,
            'password': password,
        }
        url = url_for('auth.login')
        response = self.client.post(url, data=data, follow_redirects=True)
        return response

    def test_auth(self):
        target = User(email='704364447@qq.com',
                    username='admin',
                    password='123')
        form = RegistrationForm(formdata=None, obj=target)
        data = {
            'email': '704364447@qq.com',
            'username': 'admin',
            'password': '123',
            'password2': '123',
        }

        url = url_for('auth.register')
        response = self.client.post(url, data=data)
        assert response.status_code == 302
        user = User.query.filter_by(username=target.username).first()
        assert user

        url = url_for('auth.login')
        response = self.login('admin', '123')
        assert response.status_code == 200
        assert re.search('Hello,\s+admin!', response.get_data(as_text=True))

        url = url_for('auth.logout')
        response = self.client.get(url, follow_redirects=True)
        assert response.status_code == 200
        assert 'You have been logged out' in response.get_data(as_text=True)

    def test_follow_logic(self):
        u1 = User(email='john@example.com', password='cat')
        u2 = User(email='susan@example.org', password='dog')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertFalse(u1.is_followed_by(u2))
        timestamp_before = datetime.utcnow()
        u1.follow(u2)
        db.session.commit()
        timestamp_after = datetime.utcnow()
        self.assertTrue(u1.is_following(u2))
        self.assertFalse(u1.is_followed_by(u2))
        self.assertTrue(u2.is_followed_by(u1))
        self.assertTrue(u1.followeds.count() == 1)
        self.assertTrue(u2.followers.count() == 1)
        f = u1.followeds.all()[-1]
        self.assertTrue(f.followed == u2)
        self.assertTrue(timestamp_before <= f.timestamp <= timestamp_after)
        f = u2.followers.all()[-1]
        self.assertTrue(f.follower == u1)
        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertFalse(u1.is_followed_by(u2))
        self.assertFalse(u2.is_following(u1))
        self.assertFalse(u2.is_followed_by(u1))
        self.assertTrue(u1.followeds.count() == 0)
        self.assertTrue(u2.followers.count() == 0)
        self.assertTrue(Follow.query.count() == 0)
        u2.follow(u1)
        db.session.commit()
        db.session.delete(u2)
        db.session.commit()
        self.assertTrue(Follow.query.count() == 0)

    def test_follow_req(self):
        follower = User(username='follower', password='cat')
        followed = User(username='followed', password='dog')
        db.session.add(follower)
        db.session.add(followed)
        db.session.commit()

        self.login('follower', 'cat')

        url = url_for('main.follow')
        data = {
            'followed_id': followed.id,
        }
        response = self.client.post(url, data=data)
        assert response.status_code == 200
        self.assertTrue(follower.is_following(followed))

    def test_unfollow_req(self):
        follower = User(username='follower', password='cat')
        followed = User(username='followed', password='dog')
        db.session.add(follower)
        db.session.add(followed)
        db.session.commit()
        self.login('follower', 'cat')
        follower.follow(followed)
        db.session.commit()

        url = url_for('main.unfollow')
        data = {
            'followed_id': followed.id,
        }
        response = self.client.post(url, data=data)
        assert response.status_code == 200
        self.assertFalse(follower.is_following(followed))
