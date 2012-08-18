# test for image cut into two pieces vertically

import os.path
import unittest

import scissors.

class Mixin(object):
    def setUp(self):
        """Before each test, set up the scissors"""
        self.app = chill.app.make_app(config=TEST_CFG, debug=True)
        self.test_client = self.app.test_client()

    def tearDown(self):
        """Get rid of the database again after each test."""
        pass

class SimpleCuts(Mixin, unittest.TestCase):

    def test_one_vertical(self):
        """A single vertical cut"""

        # all get the same page
        rv = self.test_client.get('/index.html', follow_redirects=True)
        assert 'stuff goes here' in rv.data
        rv = self.test_client.get('/')
        assert 'stuff goes here' in rv.data

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SimpleCuts))
    #add others
    return suite


if __name__ == '__main__':
    unittest.main()

