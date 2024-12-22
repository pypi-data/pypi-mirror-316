import os
import sys

from setuptools import setup
from setuptools.command.install import install
import subprocess


def get_virtualenv_path():
    """Used to work out path to install compiled binaries to."""
    if hasattr(sys, 'real_prefix'):
        return sys.prefix

    if hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix:
        return sys.prefix

    if 'conda' in sys.prefix:
        return sys.prefix

    return None


def compile_and_install_software():
    """Used the subprocess module to compile/install the C software."""
    src_path = 'exiftoolpy/exiftool-13.10'
    # copy folder to 

    # compile the software
    cmd = "make install"
    subprocess.run("ls")
    subprocess.run(["ls", "exiftoolpy"])
    subprocess.run("pwd")
    subprocess.run(cmd, cwd=src_path, shell=True)


class CustomInstall(install):
    """Custom handler for the 'install' command."""

    def run(self):
        compile_and_install_software()
        super().run()


setup(
    name='exiftoolpy',
    version='1.0',
    description='exiftoolpy',
    author='Mahmoud Lababidi',
    author_email='mahmoud@mahmoud.one',
    url='https://github.com/lababidi/exiftoolpy',
    packages=['exiftoolpy'],
    package_data={
        'exifperl': ['*.zip'],  # include all files in the perl folder
    },
    include_package_data=True,
    cmdclass={'install': CustomInstall})


# [build-system]
# requires = ["setuptools>=45", "wheel"]
# build-backend = "setuptools.build_meta"
