try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from azurectl.version import __VERSION__

config = {
    'description': 'Manage Azure PubCloud Service',
    'author': 'PubCloud Development team',
    'url': 'https://github.com/SUSE/azurectl',
    'download_url': 'https://github.com/SUSE/azurectl',
    'author_email': 'public-cloud-dev@susecloud.net',
    'version': __VERSION__,
    'install_requires': [
        'docopt==0.6.2',
        'APScheduler==3.0.2',
        'pyliblzma==0.5.3',
        'azure==0.10.2',
        'python-dateutil==2.1'
    ],
    'packages': ['azurectl'],
    'entry_points': {
        'console_scripts': ['azurectl=azurectl.azurectl:main'],
    },
    'name': 'azurectl'
}

setup(**config)
