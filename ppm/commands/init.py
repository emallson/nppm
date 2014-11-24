import os
import semver
import json
from collections import OrderedDict


prompts = OrderedDict([
    ('name', {
        'default': os.path.basename(os.getcwd()),
        'label': 'name'
    }),
    ('version', {
        'default': '1.0.0',
        'validator': semver.parse,
        'label': 'version'
    }),
    ('description', {
        'default': '',
        'label': 'description',
    }),
    ('main', {
        'default': 'main.py',
        'label': 'entry point'
    }),
    ('test', {
        'default': '',
        'label': 'test command'
    }),
    ('repository', {
        'default': '',
        'label': 'git repository'
    }),
    ('keywords', {
        'default': '',
        'label': 'keywords'
    }),
    ('author', {
        'default': '',
        'label': 'author'
    }),
    ('license', {
        'default': 'GPL',
        'label': 'license'
    }),
])


def prompt(key):

    result = input('{label}: ({default}) '
                   .format(**prompts[key])) or prompts[key]['default']

    if 'validator' in prompts[key]:
        try:
            if not prompts[key]['validator'](result):
                print('Invalid Input')
                return prompt(key)
            else:
                return result
        except ValueError:
            print('Invalid Input')
            return prompt(key)
    else:
        return result


def run_prompt(package_root, package):

    for key in prompts:
        package[key] = prompt(key)

    return package


def run_init(ns, package_root, package):
    package = run_prompt(package_root, package)
    filepath = os.path.join(package_root, 'package.json')

    print('About to write {path}:'.format(path=filepath))
    print()
    print(json.dumps(package, indent=2))

    ok = input("Is this ok? (yes) ") or 'yes'

    if ok[0].lower() == 'y':
        with open(filepath, 'w') as f:
            json.dump(package, f, indent=2)
    else:
        print('Aborted.')
