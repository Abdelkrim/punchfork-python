# Punchfork API reference: http://punchfork.com/api

import datetime
import json
import requests
from collections import namedtuple


API_BASE = 'http://api.punchfork.com/'
SSL_API_BASE = 'https://api.punchfork.com'
USER_AGENT = 'python-punchfork-api/0.1'


RecipeCollection = namedtuple('RecipeCollection',
                              ['count',
                               'recipes',
                               'next_cursor',
                               'total'])


RecipeRecord = namedtuple('Recipe',
                          ['rating',
                           'source_name',
                           'thumb',
                           'title',
                           'source_url',
                           'pf_url',
                           'published',
                           'source_img',
                           'shortcode',
                           'twc',
                           'fbc',
                           'suc',
                           'source_ingred',
                           'cat_ingred',
                           'canon_ingred'])


PublisherRecord = namedtuple('Publisher',
                             ['name',
                              'twitter',
                              'site',
                              'num_recipes',
                              'avatar',
                              'avg_rating'])


DietIndex = namedtuple('DietIndex', ['diets', 'alerts'])


class Client(object):
    """Punchfork API client."""
    def __init__(self, api_key, use_ssl=False):
        self.api_key = api_key
        self.api_base = SSL_API_BASE if use_ssl else API_BASE

    def request_with_key(self, endpoint, params={}):
        """Add an API key to the request, and make the call to the
        given endpoint."""
        params['key'] = self.api_key
        req = self.api_base + endpoint
        result = requests.get(req, headers={'User-Agent': USER_AGENT}, params=params)
        res = json.loads(result.content)
        if result.status_code == 200:
            return res
        else:
            raise Exception(res['error'])

    def search(self, searchterm, ingred=None, count=None, cursor=None, sort=None,
               publisher=None, likes=None, startdate=None, enddate=None, total=None):
        """Search recipes."""
        endpoint = '/recipes'
        params = {'q': searchterm}

        if ingred:
            params['ingred'] = ingred

        if count:
            params['count'] = count

        if cursor:
            params['cursor'] = cursor

        if sort:
            params['sort'] = sort

        if publisher:
            params['from'] = publisher

        if likes:
            params['likes'] = likes

        if startdate:
            assert isinstance(startdate, datetime.datetime)
            params['startdate'] = startdate

        if enddate:
            assert isinstance(enddate, datetime.datetime)
            params['enddate'] = enddate

        if total:
            params['total'] = total

        res = self.request_with_key(endpoint, params)
        recipes = RecipeCollection(res.get('count'),
                                   [RecipeRecord(r.get('rating'),
                                                 r.get('source_name'),
                                                 r.get('thumb'),
                                                 r.get('title'),
                                                 r.get('source_url'),
                                                 r.get('pf_url'),
                                                 r.get('published'),
                                                 r.get('source_img'),
                                                 r.get('shortcode'),
                                                 r.get('twc'),
                                                 r.get('fbc'),
                                                 r.get('suc'),
                                                 r.get('source_ingred'),
                                                 r.get('cat_ingred'),
                                                 r.get('canon_ingred')) for r in res['recipes']],
                                   res.get('next_cursor'),
                                   res.get('total'))
        return recipes

    def random_recipe(self):
        """Return a random recipe."""
        endpoint = '/random_recipe'
        res = self.request_with_key(endpoint)
        r = res['recipe']
        recipe = RecipeRecord(r.get('rating'),
                              r.get('source_name'),
                              r.get('thumb'),
                              r.get('title'),
                              r.get('source_url'),
                              r.get('pf_url'),
                              r.get('published'),
                              r.get('source_img'),
                              r.get('shortcode'),
                              r.get('twc'),
                              r.get('fbc'),
                              r.get('suc'),
                              r.get('source_ingred'),
                              r.get('cat_ingred'),
                              r.get('canon_ingred'))
        return recipe

    def list_publishers(self):
        """Return the list of publishers."""
        endpoint = '/publishers'
        res = self.request_with_key(endpoint)
        publishers = [PublisherRecord(**p) for p in res['publishers']]
        return publishers

    def rate_limit_status(self):
        """Return the rate limit status of the API key."""
        endpoint = '/rate_limit_status'
        status = self.request_with_key(endpoint)
        return status['remaining_calls']

    def generate_diet_index(self, ingredients):
        """Generate a diet index for a list of ingredients."""
        endpoint = '/diet_index'
        params = {'ingred': ingredients}
        response = self.request_with_key(endpoint, params)
        return DietIndex(response.get('diets'), response.get('alerts', []))
