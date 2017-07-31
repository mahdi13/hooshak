import pymlconf
from os.path import abspath

settings = pymlconf.DeferredConfigManager()

BUILTIN_CONFIGURATION = """

csv:
  delimiter: ','

amazon:
  csv: %(root_path)s/datasource/beautiful_ratings_Movies_and_TV_reverse.csv
  # lines_to_learn: 2000000
  # lines_to_predict: 10000
  lines_to_learn: 200000
  lines_to_predict: 1000


debug: true
"""

# TODO: `Context` should effect when getting dynamically


_context = {
    'root_path': abspath('../../')
}

settings.load(builtin=BUILTIN_CONFIGURATION, context=_context)
