import json
from collections import OrderedDict


def merge(old_dict, new_dict):
    return dict(list(old_dict.items()) + list(new_dict.items()))


def pkg_load(f):
    return json.load(f, object_pairs_hook=OrderedDict)
