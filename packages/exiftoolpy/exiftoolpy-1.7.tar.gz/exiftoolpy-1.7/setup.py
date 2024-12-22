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
    try:
        subprocess.run(["apt-get", "update"])
        subprocess.run(["apt-get", "install", "-y",  "poppler-utils"])
    except Exception as e:
        if "no such" in str(e).lower():
            print(e)
            pass
        else:
            raise


class CustomInstall(install):
    """Custom handler for the 'install' command."""

    def run(self):
        compile_and_install_software()
        super().run()


setup(
    name='exiftoolpy',
    version='1.7',
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
