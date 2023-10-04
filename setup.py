from setuptools import setup, find_packages

from lnarcade.version import VERSION

setup(
    name='arcade menu system',
    version=VERSION,
    description='A lightning-powered arcade entertainment menu system.',
    author='Micah Fullerton',
    author_email='plebeiusgaragicus@gmail.com',
    url='https://github.com/PlebeiusGaragicus/arcade-game-menu',
    packages=find_packages(),
    install_requires=[
        # List your app's dependencies here
        # 'docopt',
        'arcade',
    ],
    classifiers=[
        # Choose classifiers from https://pypi.org/classifiers/
        # TODO:
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
