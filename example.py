import punchfork

# You can find your API key at http://punchfork.com/api
api_key = 'YOUR_API_KEY_HERE'

# Create the Punchfork client
client = punchfork.Client(api_key)

# Try a search!
search_results = client.search('tomato basil olive oil')

print "There were {} results".format(search_results.count)
print

for recipe in search_results.recipes:
    print "Recipe:", recipe.title
    print "Source URL:", recipe.source_url
    print

# You can also view a list of publishers
publisher_list = client.list_publishers()

for publisher in publisher_list:
    print "Publisher: {}, {}".format(publisher.name, publisher.site)

print

# Get a random recipe
random_recipe = client.random_recipe()
print 'The random recipe was: "{}", and can be found at {}'.format(random_recipe.title, random_recipe.pf_url)
print

# Find out how many API calls you have remaining in your rate limit
print client.rate_limit_status(), "API calls remaining"
