try:
  # Prefer simplejson for speed.
  from simplejson import *
except (ImportError, SyntaxError):
  # On Python/PyPy 3.2 simplejson is broken
  from json import *

