from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):
    
    def setUp(self):
        """Before every test do this things"""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Making sure if the info is displayed and added to session"""

        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('numplays'))
            self.assertIn(b'Highest Score:', response.data)
            self.assertIn(b'Number of Plays:', response.data)
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'Time Left:', response.data)
            
    def test_valid_word(self):
        """Testing if word is valid on board"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [
                    ['C', 'A', 'R', 'G', 'D'],
                    ['C', 'A', 'R', 'G', 'D'],
                    ['C', 'A', 'R', 'G', 'D'],
                    ['C', 'A', 'R', 'G', 'D'],
                    ['C', 'A', 'R', 'G', 'D']
                ]
        response = self.client.get('check-word?word=car')
        self.assertEqual(response.json['result'], 'ok')

    def test_not_on_board(self):
        """Testing if word is not on board"""

        self.client.get('/')
        response = self.client.get('/check-word?word=apple')
        self.assertEqual(response.json['result'], 'not-on-board')

    def test_not_a_word(self):
        """Testing if word is not english word"""

        self.client.get('/')
        response = self.client.get('/check-word?word=adksf')
        self.assertEqual(response.json['result'], 'not-word')

   