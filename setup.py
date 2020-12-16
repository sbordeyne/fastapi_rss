from setuptools import setup

from fastapi_rss import __version__


with open('requirements.txt', 'r') as f:
    requirements = [line for line in f]


setup(
    name='fastapi_rss',
    version=__version__,
    author='Dogeek',
    url='https://github.com/Dogeek/fastapi_rss/',
    description='A library to generate RSS feeds for FastAPI',
    python_requires='>=3.6.5',
    install_requires=requirements,
    zip_safe=True,
    platforms='any',
)
