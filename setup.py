try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Manage Azure PubCloud Service',
    'author': 'PubCloud Development team',
    'url': 'https://github.com/SUSE/azure-cli',
    'download_url': 'https://github.com/SUSE/azure-cli',
    'author_email': 'public-cloud-dev@suse.de',
    'version': '0.8.1.5',
    'install_requires': ['docopt', 'APScheduler'],
    'packages': ['azure_cli'],
    'entry_points': {
        'console_scripts': ['azure-cli=azure_cli.azure_cli:main'],
    },
    'name': 'azure_cli'
}

setup(**config)
