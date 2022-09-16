from os import path
from setuptools import setup

with open(path.join(path.dirname(path.abspath(__file__)), 'README.rst')) as f:
    readme = f.read()

setup(
    name             = 'timestampmaker',
    version          = '0.1.0',
    description      = 'Create timestamps for the ChRIS project(s).',
    long_description = readme,
    author           = 'barbacbd',
    author_email     = 'bbarbach@redhat.com',
    url              = 'https://github.com/rh-impact/pl-timestampmaker',
    packages         = ['timestampmaker'],
    install_requires = ['chrisapp'],
    test_suite       = 'nose.collector',
    tests_require    = ['nose', 'mock'],
    license          = 'MIT',
    zip_safe         = False,
    python_requires  = '>=3.6',
    entry_points     = {
        'console_scripts': [
            'timestampmaker = timestampmaker.__main__:main'
            ]
        }
)
