import os
import subprocess

from nppm.util import merge


def make_pythonpath(package_root, package):
    base = [os.path.join(package_root, "python_modules/")]
    if 'directories' in package and 'lib' in package['directories']:
        base += [os.path.join(package_root, package['directories']['lib'])]
    return ':'.join(base)


def python(args, package_root, package):
    if package_root:
        env = merge(
            os.environ,
            {"PYTHONPATH": make_pythonpath(package_root, package)}
        )

    else:
        env = os.environ
    process = subprocess.Popen(['/usr/bin/ipython3'] + args, env=env)
    process.wait()


def run_main(ns, package_root, package):
    python([package['main']] + ns.args, package_root, package)


def run_python(ns, package_root, package):
    python(ns.args, package_root, package)
