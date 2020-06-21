import ast
import codecs
import re
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))


def read(*parts):
    with codecs.open(path.join(here, *parts), 'r') as fp:
        return fp.read()


_version_re = re.compile(r"__version__\s+=\s+(.*)")


def find_version(*where):
    return str(ast.literal_eval(_version_re.search(read(*where)).group(1)))


long_description = read('README.rst')

base_reqs = [
    'Falcon',
    'Pony',
    'Marshmallow',
    'python-dotenv',
]

test_reqs = [
    'pytest',
    'pytest-mock',
    'pytest-cov',
    'pytest-factoryboy',
]

docs_reqs = [
    'Sphinx',
]

dev_reqs = [
    'ipython',
    'ipdb',
    'pip',
    'setuptools',
    'wheel',
    'flake8',
    'flake8-builtins',
    'flake8-bugbear',
    'flake8-mutable',
    'flake8-comprehensions',
    'pep8-naming',
    'dlint',
    'rstcheck',
    'rope',
    'isort',
    'werkzeug[watchdog]',
] + test_reqs + docs_reqs

setup(
    name='bbbrating',
    version=find_version('src', 'bbbr', '__version__.py'),
    author='Jarek Zgoda',
    author_email='jarek.zgoda@gmail.com',
    description='Browar.biz beer rating application (backend)',
    keywords='beer rating',
    long_description=long_description,
    license='BSD',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    url='http://github.com/zgoda/bbbrating-server',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Content Management System',
    ],
    install_requires=base_reqs,
    extras_require={
        'prod': [
            'gunicorn',
        ],
        'dev': dev_reqs,
        'test': test_reqs,
        'docs': docs_reqs,
    },
    entry_points={
        'console_scripts': [
            'rating=bbbr.cli:main',
        ]
    },
    python_requires='~=3.7',
)
