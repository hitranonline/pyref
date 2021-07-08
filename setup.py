#   Copyright 2020 Frances M. Skinner, Christian Hill
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# Project uses reStructuredText, so ensure that the docutils get
# installed or upgraded on the target machine
install_requires=["docutils>=0.3"],

setup(
    name='refs',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='Apache Software Foundation',
    description='An automatic referencing system for scientific databases',
    long_description=README,
    keywords="database, HITRAN, reference, citation",
    url='https://github.com/hitranonline',
    author='Frances Skinner, Iouli Gordon, Christian Hill, Robert Hargreaves and Kelly Lockhart',
    author_email='hitran-admin@cfa.harvard.edu',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11.8',
        'Intended Audience :: Developers',
        'License :: Apache License, Version 2.0', 
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
