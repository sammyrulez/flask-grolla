import unittest
from flask import Flask
from flask_grolla import TwitterAuth


app = Flask(__name__)

class TwitterTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.twitter = TwitterAuth(self.app,'123','456')



    def test_something(self):
        self.assertTrue(self.twitter)


if __name__ == '__main__':
    unittest.main()
