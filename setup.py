from setuptools import setup

from fastapi_rss import __version__


with open('requirements.txt', 'r') as f:
    requirements = [line for line in f]

with open('readme.md', 'r') as f:
    readme = f.read()


setup(
    name='fastapi_rss',
    packages=['fastapi_rss', 'fastapi_rss.models'],
    license='MIT',
    version=__version__,
    author='Dogeek',
    url='https://github.com/Dogeek/fastapi_rss/',
    description='A library to generate RSS feeds for FastAPI',
    long_description=readme,
    long_description_content_type='text/markdown',
    python_requires='>=3.6.5',
    install_requires=requirements,
    zip_safe=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    platforms='any',
)
