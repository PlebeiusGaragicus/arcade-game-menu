from setuptools import setup, find_packages

# from lnarcade.version import VERSION # we don't do it this way as it causes import errors during `pip3 install -e .`
VERSION = '0.0.4'

setup(
    name='lightning arcade system',
    version=VERSION,
    description='A lightning-powered arcade entertainment menu system.',
    author='Micah Fullerton',
    author_email='plebeiusgaragicus@gmail.com',
    url='https://github.com/PlebeiusGaragicus/arcade-game-menu',
    packages=find_packages(),
    install_requires=[
        'arcade',
        'python-dotenv',
    ],
    classifiers=[
        # Choose classifiers from https://pypi.org/classifiers/
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    entry_points={
        'console_scripts': [
            'lnarcade=lnarcade:main',
        ],
    },
)
