#!/usr/bin/env python
# Copyright 2011 The greplin-twisted-utils Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Setup script for greplin-twisted-utils."""

try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

setup(name='scales',
      version='1.0.3',
      description='Stats for Python processes',
      license='Apache',
      author='Greplin, Inc.',
      author_email='opensource@greplin.com',
      url='https://www.github.com/Cue/scales',
      package_dir = {'':'src'},
      packages = [
        'greplin',
        'greplin.scales',
      ],
      namespace_packages = [
        'greplin',
      ],
      install_requires=['six'],
      test_suite = 'nose.collector',
      zip_safe = True
)
