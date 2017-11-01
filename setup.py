from setuptools import setup, find_packages

from pip.req import parse_requirements
from pip.download import PipSession
import os

def read_requirements():
    '''parses requirements from requirements.txt'''
    install_reqs = parse_requirements('requirements.txt', session=PipSession())
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
      entry_points={
          'console_scripts': [
            'pysubtitles = pysubtitles.pysubtitles:main',
          ],
      }
)
