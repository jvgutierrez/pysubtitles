import os
import sys
from setuptools import setup, find_packages

from pip.req import parse_requirements
from pip.download import PipSession
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ['--cov=pysubtitles', '--cov-report',
                            'term-missing', '-v', '-s', '--flake8', '--pylint']

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

def read_requirements(filename='requirements.txt'):
    '''parses requirements from requirements.txt'''
    install_reqs = parse_requirements(filename, session=PipSession())
    reqs = [str(ir.req) for ir in install_reqs]
    return reqs

setup(name='pysubtitles',
      version='0.1',
      license='MIT',
      classifiers=['Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7',
                   'Topic :: Multimedia',
      ],
      packages=find_packages(),
      install_requires=read_requirements(),
      tests_require=read_requirements('test_requirements.txt'),
      entry_points={
          'console_scripts': [
            'pysubtitles = pysubtitles.pysubtitles:main',
          ],
      },
      cmdclass={'test': PyTest},
)
