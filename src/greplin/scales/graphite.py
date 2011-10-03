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

"""Tools for pushing stat values to graphite."""

from greplin import scales
from greplin.scales import util

import os
import threading
import time



class GraphitePeriodicPusher(threading.Thread):
  """A thread that periodically pushes all stat values to Graphite."""

  def __init__(self, host, port, prefix, period=60):
    """If prefix is given, it will be prepended to all Graphite
    stats. If it is not given, then a prefix will be derived from the
    hostname."""
    threading.Thread.__init__(self)
    self.daemon = True

    self.period = period
    self.forbidden = set()
    self.rules = []

    self.prefix = prefix

    if self.prefix and self.prefix[-1] != '.':
      self.prefix += '.'

    self.oldPrefix = None
    self.graphite = util.GraphiteReporter(host, port)


  def run(self):
    """Loop forever, pushing out stats."""
    self.graphite.start()
    while True:
      time.sleep(self.period)
      self._push()


  def _sanitize(self, name):
    """Sanitize a name for graphite."""
    return name.strip().replace(' ', '-').replace('.', '-')


  def _push(self, statsDict=None, prefix=None, path=None):
    """Push stat values out to Graphite."""
    if statsDict is None:
      statsDict = scales.getStats()
    prefix = prefix or self.prefix
    path = path or '/'

    for name, value in statsDict.iteritems():
      name = str(name)
      subpath = os.path.join(path, name)
      if subpath in self.forbidden:
        continue
      if hasattr(value, 'iteritems'):
        self._push(value, '%s%s.' % (prefix, self._sanitize(name)), subpath)
      else:
        if hasattr(value, '__call__'):
          value = value()
        for rule in self.rules:
          if not rule(name, value):
            break
        else:
          if type(value) in [int, long, float] and len(name) < 500:
            self.graphite.log(prefix + self._sanitize(name), value)


  def doNotLog(self, prefix = None):
    """Do not log stats beginning with prefix."""
    if prefix:
      self.forbidden.add(prefix.strip())


  def addLogRule(self, rule):
    """Adds a rule function that when given a name and a value, decides whether to log it or not."""
    self.rules.append(rule)
