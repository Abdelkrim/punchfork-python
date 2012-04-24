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
        self.assertGreater(search_results.count, 0)
        self.assertGreater(search_results.recipes.count, 0)

    def test_with_ingred(self):
        search_results = self.client.search('apple', ingred=True)
        self.assertGreater(len(search_results.recipes[0].source_ingred), 0)
        self.assertGreater(len(search_results.recipes[0].cat_ingred), 0)
        self.assertGreater(len(search_results.recipes[0].canon_ingred), 0)

    def test_with_count(self):
        search_results = self.client.search('apple', count=25)
        self.assertEqual(search_results.count, 25)

    def test_with_cursor(self):
        search_results = self.client.search('apple')
        first_record = search_results.recipes[0]
        next_page = self.client.search('apple', cursor=10)
        next_record = next_page.recipes[0]
        self.assertNotEqual(first_record, next_record)

    def test_with_sort(self):
        #pmn: this test needs to be improved
        search_results = self.client.search('apple', sort='d')
        self.assertGreater(search_results.count, 0)

    def test_wtih_likes(self):
        #pmn: this test needs to be improved
        search_results = self.client.search('beef', likes='pmn')
        self.assertGreater(search_results.count, 0)

    def test_from_publisher(self):
        #pmn: this test needs to be improved
        search_results = self.client.search('apple', publisher='The Pioneer Woman')
        self.assertGreater(search_results.count, 0)

    def test_with_startdate(self):
        #pmn: this test needs to be improved
        startdate = datetime.datetime.now() - datetime.timedelta(days=365)
        search_results = self.client.search('apple', startdate=startdate)
        self.assertGreater(search_results.count, 0)

    def test_with_enddate(self):
        #pmn: this test needs to be improved
        enddate = datetime.datetime.now() - datetime.timedelta(days=365)
        search_results = self.client.search('apple', enddate=enddate)
        self.assertGreater(search_results.count, 0)

    def test_with_total(self):
        search_results = self.client.search('apple', total=True)
        self.assertGreater(search_results.total, 0)


class TestRandomRecipe(PunchforkTestCase):
    def test_basic(self):
        recipe = self.client.random_recipe()
        self.assertGreater(len(recipe.title), 0)


class TestListPublishers(PunchforkTestCase):
    def test_basic(self):
        publishers = self.client.list_publishers()
        self.assertGreater(publishers.count, 0)
        self.assertGreater(len(publishers[0].name), 0)


class TestRateLimitStatus(PunchforkTestCase):
    def test_basic(self):
        rate_limit_status = self.client.rate_limit_status()
        self.assertGreaterEqual(rate_limit_status, 0)


class TestGenerateDietIndex(PunchforkTestCase):
    def test_basic(self):
        diet_index = self.client.generate_diet_index('''2 cups yellow cornmeal
2 teaspoons baking powder
3/4 to 1 teaspoon fine sea salt
1 large egg, lightly beaten
1 cup water, plus more if needed
1/4 to 1/3 cup mild-flavored vegetable oil for frying''')
        self.assertEqual(diet_index, punchfork.client.DietIndex(['gluten free', 'vegetarian'], []))


if __name__ == '__main__':
    unittest.main()
