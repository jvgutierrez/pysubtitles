from functools import wraps
import json
import os.path
import time
from datetime import (
    datetime,
    timedelta,
)


def cached(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        cache_file = os.path.expanduser('~/.pysubtitles/{0}.{1}.json'.format(f.__module__, f.__name__))
        try:
            if (datetime.fromtimestamp(time.time()) - datetime.fromtimestamp(os.path.getmtime(cache_file))).days < 4:
                return json.load(open(cache_file))
        except (IOError, OSError):
            pass
        data = f(*args, **kwargs)
        json.dump(data, open(cache_file, 'w'))
        return data

    return wrapper