"""

"""
import os
from setuptools import setup
from distutils.core import Command as BaseCommand
from unittest import TestLoader, TextTestRunner


class TestCommand(BaseCommand):
    """Runs the package tests."""
    description = 'Runs all package tests.'

    user_options = [
        ('junit=', None,
         'outputs results to an xml file.')
    ]

    def initialize_options(self):
        self.junit = None

    def finalize_options(self):
        pass

    def run(self):
        # Import xmlrunner here so it's not a setup requirement
        import xmlrunner
        test_suite = TestLoader().discover('.')
        if self.junit:
            with open(self.junit, 'wb') as output:
                runner = xmlrunner.XMLTestRunner(output)
                runner.run(test_suite)
        else:
            runner = TextTestRunner(verbosity=2)
            runner.run(test_suite)

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.rst')) as f:
    long_description = f.read()

setup(name='gsf',
      version='1.0.2',
      description='GSF Py',
      long_description=long_description,
      url='https://github.com/geospatial-services-framework/gsfpy',
      author='Exelis Visual Information Solutions, Inc.',
      packages=['gsf',
                'gsf.ese'],
      cmdclass=dict(test=TestCommand),
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
