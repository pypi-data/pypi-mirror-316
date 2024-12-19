from setuptools import setup, find_packages
from os import path
working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'discord-embeds-pagination',
    version = '0.0.7',
    url = 'https://github.com/omaxpy/discord-embeds-pagination',
    author = 'omaxpy',
    author_email = 'moukasland@gmail.com',
    description = 'Pagination for embeds in discord.py bots',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    packages = find_packages(),
    install_requires = [
        "discord.py==2.4.0",
    ],
    classifiers = [
        "Programming Language :: Python :: 3",
    ]
)