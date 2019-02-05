#! /usr/bin/python
from setuptools import setup

# to install type:
# python setup.py install --root=/
def readme():
    with open('README.md') as f:
        return f.read()

setup (name='alyahmor', version='0.1',
      description='Alyahmor Arabic Morphological Genrator for Python',
      long_description = readme(),      
      author='Taha Zerrouki',
      author_email='taha. zerrouki@gmail .com',
      url='http://alyahmor.sourceforge.net/',
      license='GPL',
      package_dir={'alyahmor': 'alyahmor',},
      packages=['alyahmor'],
      include_package_data=True,
      install_requires=[ 'libqutrub>=1.0',
						'pyarabic>=0.6.2',
      ],         
      package_data = {
        'alyahmor': ['doc/*.*', 'data/*.*'],
        },
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Natural Language :: Arabic',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Text Processing :: Linguistic',
          ],
    );

