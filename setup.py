"""

"""
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.rst')) as f:
    long_description = f.read()

setup(name='gsf',
      version='2.0.0',
      description='GSF Py',
      long_description=long_description,
      url='https://github.com/geospatial-services-framework/gsfpy',
      author='Exelis Visual Information Solutions, Inc.',
      author_email='gsf@harris.com',
      install_requires=['requests'],
      packages=find_packages(),
      license='MIT',
      keywords='gsf envi idl',
      package_data = {
                  'gsf' : [
                        'doc/_modules/*.html',
                        'doc/_modules/gsf/*.html',
                        'doc/_static/*',
                        'doc/*.html',
                        'doc/*.js'
                  ]
            }
      )
