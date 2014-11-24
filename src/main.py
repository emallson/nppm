#!/usr/bin/env python3
import json
import argparse
import subprocess
import os
import pip.commands
import re
import shutil


def merge(old_dict, new_dict):
    return dict(list(old_dict.items()) + list(new_dict.items()))


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
            return json.load(pkgfile)
    except FileNotFoundError:
        return None


def install(package_root, packages):
    # monkey patching shutil.move b/c it throws an error which the install
    # command should catch and ignore -- which it doesn't, it catches and
    # prints the trace
    orig_move = shutil.move

    def stupid_move(*args):
        try:
            orig_move(*args)
        except shutil.Error as e:
            if not re.match(r"Destination path '.+' already exists", str(e)):
                raise e

    shutil.move = stupid_move

    retval = pip.commands['install']().main(
        ['--target', os.path.join(package_root, "python_modules/")] +
        packages)

    # now undo the hack
    shutil.move = orig_move

    return retval


def run_install(ns, package_root, package):
    if len(ns.packages) > 0:
        packages = ns.packages
    else:
        packages = [name + version for name, version
                    in package['dependencies'].items()]

    if install(package_root, packages) != 0:
        print("Package install failed")
        return

    def name(package):
        return re.match('[\w-]+', package).group(0)

    def version(package):
        return re.match('[\w-]+(.*)', package).group(1)

    if(ns.save):
        package['dependencies'] = merge(package.get('dependencies', {}),
                                        {name(package): version(package)
                                         for package in packages})

        with open(os.path.join(package_root, 'package.json'), 'w') as f:
            json.dump(package, f, indent=2, sort_keys=True)


def python(args, package_root):
    if package_root:
        env = merge(
            os.environ,
            {"PYTHONPATH": os.path.join(package_root, "python_modules/")}
        )

    else:
        env = os.environ
    process = subprocess.Popen(['/usr/bin/ipython3'] + args, env=env)
    process.wait()


def run_main(ns, package_root, package):
    python([package['main']] + ns.args, package_root)


def run_python(ns, package_root, package):
    python(ns.args, package_root)


def main():
    parser = argparse.ArgumentParser(description="NPM for Python")
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

    args = parser.parse_args()
    try:
        package_root = find_package_root()
        package = load_package(package_root) or {}

        args.func(args, package_root, package)
    except(AttributeError):
        parser.print_help()

if __name__ == "__main__":
    main()
