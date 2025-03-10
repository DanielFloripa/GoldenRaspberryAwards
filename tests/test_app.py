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
            db.engine.dispose()

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
        expected = {
            "max":[
                {
                    "producer":"Producer 1",
                    "interval":99, # Correct value must be 109
                    "previousWin":1900,
                    "followingWin":1999, # Correct value must be 2009
                },
                {
                    "producer":"Producer 2",
                    "interval":99,
                    "previousWin":2000,
                    "followingWin":2099
                }
            ],
            "min":[
                {
                    "producer":"Producer 1",
                    "interval":1,
                    "previousWin":2008,
                    "followingWin":2009
                },
                {
                    "producer":"Producer 2",
                    "interval":1,
                    "previousWin":2018,
                    "followingWin":2019
                }
            ]
        }
        producers = {
            "Producer 1": [2008, 2009, 1900, 1999],
            "Producer 2": [2018, 2019, 2000, 2099],
        }
        new_movie = {
            "year": None,
            "title": "New Movie",
            "studios": "New Studio",
            "producers": None,
            "winner": 'yes'
        }
        ids_to_delete = []
        
        # insert moched data
        for producer, years in producers.items():
            new_movie["producers"] = producer
            for year in years:
                new_movie["year"] = year
                response = self.client.post('/movies', data=json.dumps(new_movie), content_type='application/json')
                ids_to_delete.append(json.loads(response.data)['id'])
        
        # get the main result
        response = self.client.get('/get_interval')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)
        
        # assert structure:
        self.assertIn('min', data)
        self.assertIn('max', data)
        for key in ['min', 'max']:
            self.assertIsInstance(data[key], list)
            for item in data[key]:
                self.assertIn('producer', item)
                self.assertIn('interval', item)
                self.assertIn('previousWin', item)
                self.assertIn('followingWin', item)
            # Assert content:
            sorted_data = sorted(data[key], key=lambda x: (x['producer'],x['previousWin']))
            sorted_expected = sorted(expected[key], key=lambda x: (x['producer'],x['previousWin']))
            for position, s_data in enumerate(sorted_data):
                self.assertDictEqual(s_data, sorted_expected[position])
        
        # clear data:
        for movie_id in ids_to_delete:
            response = self.client.delete('/movies/{}'.format(movie_id))
            self.assertEqual(response.status_code, 204)

    def test_add_movie(self):
        new_movie = {
            "year": 2021,
            "title": "New Movie",
            "studios": "New Studio",
            "producers": "New Producer",
            "winner": 'yes'
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
            "winner": 'yes'
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
            "winner": 'yes'
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
