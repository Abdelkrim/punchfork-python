import datetime
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import punchfork


API_KEY = os.environ.get('PUNCHFORK_API_KEY')


class PunchforkTestCase(unittest.TestCase):
    def setUp(self):
        self.client = punchfork.Client(API_KEY)


class TestSearch(PunchforkTestCase):
    def test_basic(self):
        search_results = self.client.search('mac & cheese')
        self.assertTrue(search_results.count > 0)
        self.assertTrue(search_results.recipes.count > 0)

    def test_with_ingred(self):
        search_results = self.client.search('apple', ingred=True)
        self.assertTrue(len(search_results.recipes[0].source_ingred) > 0)
        self.assertTrue(len(search_results.recipes[0].cat_ingred) > 0)
        self.assertTrue(len(search_results.recipes[0].canon_ingred) > 0)

    def test_with_count(self):
        search_results = self.client.search('apple', count=25)
        self.assertTrue(search_results.count == 25)

    def test_with_cursor(self):
        search_results = self.client.search('apple')
        first_record = search_results.recipes[0]
        next_page = self.client.search('apple', cursor=10)
        next_record = next_page.recipes[0]
        self.assertTrue(first_record != next_record)

    def test_with_sort(self):
        #pmn: this test needs to be improved
        search_results = self.client.search('apple', sort='d')
        self.assertTrue(search_results.count > 0)

    def test_wtih_likes(self):
        #pmn: this test needs to be improved
        search_results = self.client.search('beef', likes='pmn')
        self.assertTrue(search_results.count > 0)

    def test_from_publisher(self):
        #pmn: this test needs to be improved
        search_results = self.client.search('apple', publisher='The Pioneer Woman')
        self.assertTrue(search_results.count > 0)

    def test_with_startdate(self):
        #pmn: this test needs to be improved
        startdate = datetime.datetime.now() - datetime.timedelta(days=365)
        search_results = self.client.search('apple', startdate=startdate)
        self.assertTrue(search_results.count > 0)

    def test_with_enddate(self):
        #pmn: this test needs to be improved
        enddate = datetime.datetime.now() - datetime.timedelta(days=365)
        search_results = self.client.search('apple', enddate=enddate)
        self.assertTrue(search_results.count > 0)

    def test_with_total(self):
        search_results = self.client.search('apple', total=True)
        self.assertTrue(search_results.total > 0)

class TestRandomRecipe(PunchforkTestCase):
    def test_basic(self):
        recipe = self.client.random_recipe()
        self.assertTrue(len(recipe.title) > 0)


class TestListPublishers(PunchforkTestCase):
    def test_basic(self):
        publishers = self.client.list_publishers()
        self.assertTrue(publishers.count > 0)
        self.assertTrue(len(publishers[0].name) > 0)


class TestRateLimitStatus(PunchforkTestCase):
    def test_basic(self):
        rate_limit_status = self.client.rate_limit_status()
        self.assertTrue(rate_limit_status >= 0)


if __name__ == '__main__':
    unittest.main()
