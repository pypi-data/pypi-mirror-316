
from setuptools import setup, find_packages


version = '1.0.1'
url = 'https://github.com/pmaigutyak/mp-suppliers'

setup(
    name='django-mp-suppliers',
    version=version,
    description='Django suppliers app',
    author='Paul Maigutyak',
    author_email='pmaigutyak@gmail.com',
    url=url,
    download_url='{}/archive/{}.tar.gz'.format(url, version),
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
)
