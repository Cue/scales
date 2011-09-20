# Copyright 2011 The scales Authors.
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

"""Tests for stat formatting."""

from greplin import scales
from greplin.scales import formats

import StringIO
import unittest



class Root(object):
  """Root level test class."""

  def __init__(self):
    scales.init(self)


  def getChild(self, name, collapsed):
    """Creates a child."""
    return Child(name, collapsed)



class Child(object):
  """Child test class."""

  countStat = scales.IntStat('count')


  def __init__(self, name, collapsed):
    scales.initChild(self, name).setCollapsed(collapsed)



class StatsTest(unittest.TestCase):
  """Test cases for stats classes."""

  def setUp(self):
    """Reset global state."""
    scales.reset()


  def testJsonCollapse(self):
    """Tests for collapsed child stats."""
    r = Root()
    r.getChild('here', False).countStat += 1
    r.getChild('not', True).countStat += 100

    out = StringIO.StringIO()
    formats.jsonFormat(out)

    self.assertEquals('{"here": {"count": 1}}\n', out.getvalue())
