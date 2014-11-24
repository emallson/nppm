#!/usr/bin/env python
import argparse
import os
from collections import OrderedDict

from ppm.util import pkg_load
from ppm.commands.install import run_install
from ppm.commands.python import run_python, run_main
from ppm.commands.init import run_init


def find_package_root():
    path = os.path.abspath('.')
    files = [f for f in os.listdir(path)
             if os.path.isfile(os.path.join(path, f))]
    while 'package.json' not in files and path != '/':
        path = os.path.dirname(path)
        files = [f for f in os.listdir(path)
                 if os.path.isfile(os.path.join(path, f))]

    if path == '/':
        path = os.getcwd()
    return path


def load_package(root):
    try:
        with open(os.path.join(root, 'package.json')) as pkgfile:
            return pkg_load(pkgfile)
    except FileNotFoundError:
        return None


def main():
    parser = argparse.ArgumentParser(prog='ppm', description="npm-style package management interface for Python projects.")
    parser.add_argument('--version', action='version', version='%(prog)s 0.1.0')
    command_parsers = parser.add_subparsers(description="")

    # start [args]
    start_parser = command_parsers.add_parser('start',
                                              help='Start application',
                                              aliases=['run'])
    start_parser.add_argument("args", nargs=argparse.REMAINDER)
    start_parser.set_defaults(func=run_main)

    # install
    install_parser = command_parsers.add_parser('install',
                                                help='Install dependencies')
    install_parser.add_argument("--save", action='store_true', default=False)
    install_parser.add_argument("packages", nargs='*')
    install_parser.set_defaults(func=run_install)

    # python
    python_parser = command_parsers.add_parser(
        'python',
        help='Run IPython with the correct path',
        aliases=['repl']
    )
    python_parser.add_argument("args", nargs=argparse.REMAINDER)
    python_parser.set_defaults(func=run_python)

    # init
    init_parser = command_parsers.add_parser(
        'init',
        help='Initialize a PPM project',
    )
    init_parser.set_defaults(func=run_init)

    args = parser.parse_args()
    package_root = find_package_root()
    package = load_package(package_root) or OrderedDict()

    if hasattr(args, 'func'):
        args.func(args, package_root, package)
    else:
        parser.print_usage()

if __name__ == "__main__":
    main()
