import unittest
from app import create_app, db
from app.models import User, Product
from config import TestingConfig

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_user(self):
        response = self.client.post('/create_user', data={
            'name': 'Test User',
            'email': 'testuser@example.com',
            'dob': '1990-01-01',
            'hobby': 'Reading',
            'password': 'password123'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)  # Ensure the final status is 200 (success)
        with self.app.app_context():
            user = User.query.filter_by(email='testuser@example.com').first()
            self.assertIsNotNone(user)  # Ensure user was created

    def test_login(self):
        self.client.post('/create_user', data={
            'name': 'Test User',
            'email': 'testuser@example.com',
            'dob': '1990-01-01',
            'hobby': 'Reading',
            'password': 'password123'
        }, follow_redirects=True)

        response = self.client.post('/login', data={
            'email': 'testuser@example.com',
            'password': 'password123'
        },follow_redirects=True)

        self.assertEqual(response.status_code, 200)  # Ensure status is 200 after successful login
        self.assertIn(b'Dashboard', response.data)  # Check if the dashboard is in the response (assuming dashboard is the final page)

    def test_add_product(self):
        # self.client.post('/create_user', data={
        #     'name': 'Test User',
        #     'email': 'testuser@example.com',
        #     'dob': '1990-01-01',
        #     'hobby': 'Reading',
        #     'password': 'password123'
        # },follow_redirects=True)

        # self.client.post('/login', data={
        #     'email': 'testuser@example.com',
        #     'password': 'password123'
        # },follow_redirects=True)

        response = self.client.post('/add_product', data={
            'name': 'Test Product',
            'stock': '10'
        },follow_redirects=True)

        self.assertEqual(response.status_code, 200)  # Ensure the status is 200 after adding product
        with self.app.app_context():
            product = Product.query.filter_by(name='Test Product').first()
            self.assertIsNotNone(product)  # Ensure the product was added

if __name__ == '__main__':
    unittest.main()
