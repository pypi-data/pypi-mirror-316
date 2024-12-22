import os
from setuptools import setup, find_packages

# Read the contents of README file
with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read the requirements from requirements.txt
def read_requirements(filename):
    with open(filename) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Package meta-data
NAME = 'movie_metadata'
DESCRIPTION = 'A Python wrapper for The Movie Database (TMDB) API'
URL = 'https://github.com/AhmedOsamaMath/movie-metadata'
EMAIL = 'ahmedosamamath@gmail.com'
AUTHOR = 'Ahmed Osama'
REQUIRES_PYTHON = '>=3.7.0'
VERSION = '0.1.0'

# Required packages
REQUIRED = [
    'requests>=2.25.0',
    'typing-extensions>=4.0.0; python_version < "3.8"',
]

# Optional packages
EXTRAS = {
    'dev': [
        'pytest>=6.0',
        'pytest-cov>=2.0',
        'mypy>=0.910',
        'black>=21.0',
        'isort>=5.0',
        'flake8>=3.9',
    ],
    'docs': [
        'sphinx>=4.0',
        'sphinx-rtd-theme>=0.5',
        'myst-parser>=0.15',
    ],
}

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Multimedia :: Video',
        'Topic :: Internet :: WWW/HTTP',
    ],
    keywords='tmdb, movies, tv, api, wrapper, film, television, database, metadata',
    project_urls={
        'Bug Reports': f'{URL}/issues',
        'Documentation': f'{URL}/wiki',
        'Source': URL,
    },
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'tmdb=movie_metadata.cli:main',  # If you add CLI functionality later
        ],
    },
)