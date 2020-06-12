#!/usr/bin/env python3

from setuptools import setup, find_packages

#with open("README.md", "r") as fh:
#    long_description = fh.read()

setup(
  name='Simanfor',
  version='0.9',
  description='Simanfor tree simulator',
  packages=find_packages(),
  author='Moises Martinez (Sngular)',
  author_email='moises.martinez@sngular.com',
  long_description_content_type="text/markdown",
  url='',
  license='Apache 2',
  package_data={},
  include_package_data=True,
  python_requires='>=3.6',
  install_requires=[
    'bokeh==1.4.0',
    'Click==7.0',
    'cloudpickle==1.3.0',
    'dask==2.10.1',
    'distributed==2.10.0',
    'et-xmlfile==1.0.1',
    'fsspec==0.6.2',
    'HeapDict==1.0.1',
    'jdcal==1.4.1',
    'Jinja2==2.11.1',
    'locket==0.2.0',
    'MarkupSafe==1.1.1',
    'msgpack==0.6.2',
    'numpy==1.18.1',
    'openpyxl==3.0.3',
    'packaging==20.1',
    'pandas==1.0.1',
    'partd==1.1.0',
    'Pillow==7.0.0',
    'psutil==5.6.7',
    'pyparsing==2.4.6',
    'python-dateutil==2.8.1',
    'pytz==2019.3',
    'PyYAML==5.3',
    'scipy==1.4.1',
    'six==1.14.0',
    'sortedcontainers==2.1.0',
    'tblib==1.6.0',
    'toolz==0.10.0',
    'tornado==6.0.3',
    'xlrd==1.2.0',
    'zict==1.0.0'
  ],
)