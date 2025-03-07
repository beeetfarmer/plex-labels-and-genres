from setuptools import setup, find_packages

setup(
    name="plex-labels-and-genres",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "plexapi>=4.6.0",
        "argparse>=1.4.0",
    ],
    entry_points={
        'console_scripts': [
            'plex-metadata=scripts.plex_metadata_tool:main',
        ],
    },
    author="beeetfarmer",
    author_email="",
    description="Tool for managing Plex TV Show labels and genres",
    keywords="plex, metadata, tv shows, labels, genres",
    url="https://github.com/beeetfarmer/plex-labels-and-genres",
)