import unittest
import json
from app.main import app, db
from app.models import Movie

class MovieAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        with self.app.app_context():
            db.create_all()
            Movie.load_movies_from_csv()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.session.close()

    def test_get_movies(self):
        response = self.client.get('/movies')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_nominees(self):
        response = self.client.get('/nominees')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_winners(self):
        response = self.client.get('/winners')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_interval(self):
        response = self.client.get('/get_interval')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)
        self.assertIn('min', data)
        self.assertIn('max', data)
        for key in ['min', 'max']:
            self.assertIsInstance(data[key], list)
            for item in data[key]:
                self.assertIn('producer', item)
                self.assertIn('interval', item)
                self.assertIn('previousWin', item)
                self.assertIn('followingWin', item)

    def test_add_movie(self):
        new_movie = {
            "year": 2021,
            "title": "New Movie",
            "studios": "New Studio",
            "producers": "New Producer",
            "winner": True
        }
        response = self.client.post('/movies', data=json.dumps(new_movie), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['title'], new_movie['title'])

    def test_update_movie(self):
        new_movie = {
            "year": 2025,
            "title": "New Movie",
            "studios": "New Studio",
            "producers": "New Producer",
            "winner": True
        }
        response = self.client.post('/movies', data=json.dumps(new_movie), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        movie_id = json.loads(response.data)['id']

        updated_movie = {
            "title": "Updated Movie Title"
        }
        response = self.client.patch(
            '/movies/{}'.format(movie_id),
            data=json.dumps(updated_movie),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], updated_movie['title'])

    def test_delete_movie(self):
        new_movie = {
            "year": 2025,
            "title": "New Movie",
            "studios": "New Studio",
            "producers": "New Producer",
            "winner": True
        }
        response = self.client.post('/movies', data=json.dumps(new_movie), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        movie_id = json.loads(response.data)['id']

        response = self.client.delete('/movies/{}'.format(movie_id))
        self.assertEqual(response.status_code, 204)

        response = self.client.get('/movies/{}'.format(movie_id))
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()