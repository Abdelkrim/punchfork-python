#punchfork-python

A Python library for interacting with the Punchfork API.

## Prequisites

You must have a valid API key before using this library. You can sign up for a free key here: http://punchfork.com/api

## Installation

Install with Pip:

    pip install -e git+git://github.com/punchfork/punchfork-python#egg=punchfork

## Usage

```python
import punchfork

client = punchfork.Client('your-api-key')

search_results = client.search('macaroni n cheese')

for recipe in search_results.recipes:
    print "Recipe: ", recipe.title
    print "Source URL:", recipe.source_url
    print "Punchfork URL:", recipe.pf_url
    print "-------------------------------"
```

More examples can be found in example.py


Copyright &copy; 2012 Punchfork, Inc. See LICENSE for more information