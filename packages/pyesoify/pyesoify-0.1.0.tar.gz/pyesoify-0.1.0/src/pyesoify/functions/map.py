import sys
sys.path.append('..')

from string_factory import make_string

MAP = f"__builtins__.__getitem__({make_string('map')})"
