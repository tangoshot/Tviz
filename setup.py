#!/usr/bin/env python

from distutils.core import setup

setup(name='Tviz',
      version='0.1',
      description='Tanda Visualization Tool',
      author='Tolga Konik',
      author_email='tolgakonik@gmail.com',
      url='http://tangoshot.com',
      packages=['tviz', 'jriver','tutil', 'ui'],
	  package_dir = {'':'src'},
#	  data_files = {
#		'user':'user/*',
#		'images':'resources/images/*',	
#		'templates':'resources/templates/*'
#	  }
     )