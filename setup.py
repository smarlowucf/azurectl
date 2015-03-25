try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from azure_cli.version import __VERSION__

config = {
    'description': 'Manage Azure PubCloud Service',
    'author': 'PubCloud Development team',
    'url': 'https://github.com/SUSE/azure-cli',
    'download_url': 'https://github.com/SUSE/azure-cli',
    'author_email': 'public-cloud-dev@suse.de',
    'version': __VERSION__,
    'install_requires': ['docopt', 'APScheduler', 'pyliblzma'],
    'packages': ['azure_cli'],
    'entry_points': {
        'console_scripts': ['azurectl=azure_cli.azurectl:main'],
    },
    'name': 'azure_cli'
}

setup(**config)
