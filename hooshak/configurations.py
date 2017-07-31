import pymlconf
from os.path import abspath

settings = pymlconf.DeferredConfigManager()

BUILTIN_CONFIGURATION = """

csv:
  delimiter: ','

amazon:
  csv: %(root_path)s/datasource/beautiful_ratings_Movies_and_TV_reverse.csv


debug: true
"""

# TODO: `Context` should effect when getting dynamically


_context = {
    'root_path': abspath('../../')
}

settings.load(builtin=BUILTIN_CONFIGURATION, context=_context)
