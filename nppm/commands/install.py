import pip.commands
import re
import shutil
import os
import json

from nppm.util import merge


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
            json.dump(package, f, indent=2)
