from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

import golf_game

here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='golf-game',
    version=golf_game.__version__,
    author='havilash sivaratnam',
    tests_require=['pytest'],
    install_requires=[
        "pygame",
        "numpy"
    ],
    cmdclass={'test': PyTest},
    author_email='havilash2005@gmail.com',
    description='Golf Game with own Physics Engine',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    test_suite='golf_game.test.test_golf_game',
    classifiers=[
        'Programming Language :: Python',
    ],
    extras_require={
        'testing': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            'golf-game = golf_game.main:main'
        ]
    }
)