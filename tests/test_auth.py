import unittest
from app import create_app, db
from app.models import User, Role


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

        role_admin = Role.query.filter_by(name='Admin').first()
        if not role_admin:
            role_admin = Role(name='Admin', description='Admin role')
            db.session.add(role_admin)
            db.session.commit()

        u = User.query.filter_by(username='testadmin_auth').first()
        if not u:
            u = User(username='testadmin_auth', email='admin_auth@test.com', role='Admin')
            u.set_password('password123')
            db.session.add(u)
            db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User.query.filter_by(username='testadmin_auth').first()
        self.assertIsNotNone(u)
        self.assertTrue(u.check_password('password123'))
        self.assertFalse(u.check_password('wrongpass'))

    def test_login_logout(self):
        response = self.client.post('/auth/login', data={
            'username': 'testadmin_auth',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logged in as Admin', response.data)

        response_logout = self.client.get('/auth/logout', follow_redirects=True)
        self.assertEqual(response_logout.status_code, 200)
        self.assertIn(b'You have been logged out', response_logout.data)


if __name__ == '__main__':
    unittest.main()
