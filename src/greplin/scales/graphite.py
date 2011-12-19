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
import logging
import time
from fnmatch import fnmatch



class GraphitePusher(object):
  """A class that pushes all stat values to Graphite on-demand."""
  
  def __init__(self, host, port, prefix):
    """If prefix is given, it will be prepended to all Graphite
    stats. If it is not given, then a prefix will be derived from the
    hostname."""
    self.rules = []

    self.prefix = prefix

    if self.prefix and self.prefix[-1] != '.':
      self.prefix += '.'

    self.oldPrefix = None
    self.graphite = util.GraphiteReporter(host, port)


  def _sanitize(self, name):
    """Sanitize a name for graphite."""
    return name.strip().replace(' ', '-').replace('.', '-')


  def _forbidden(self, name, value):
    """Is a stat forbidden? Goes through the rules to find one that
    applies. Chronologically newer rules are higher-precedence than
    older ones. If no rule applies, the stat is forbidden by default."""
    if name[0] == '/':
      name = name[1:]
    for rule in reversed(self.rules):
      if isinstance(rule[1], basestring):
        if fnmatch(name, rule[1]):
          return not rule[0]
      elif rule[1](name, value):
        return not rule[0]
    return True # do not log by default


  def push(self, statsDict=None, prefix=None, path=None):
    """Push stat values out to Graphite."""
    if statsDict is None:
      statsDict = scales.getStats()
    prefix = prefix or self.prefix
    path = path or '/'

    for name, value in statsDict.iteritems():
      name = str(name)
      subpath = os.path.join(path, name)

      if hasattr(value, 'iteritems'):
        self.push(value, '%s%s.' % (prefix, self._sanitize(name)), subpath)
      else:
        if hasattr(value, '__call__'):
          try:
            value = value()
          except:                       # pylint: disable=W0702
            value = None
            logging.exception('Error when calling stat function for graphite push')
        if self._forbidden(subpath, value):
          continue
        else:
          if type(value) in [int, long, float] and len(name) < 500:
            self.graphite.log(prefix + self._sanitize(name), value)


  def _addRule(self, isWhitelist, rule):
    """Add an (isWhitelist, rule) pair to the rule list."""
    if isinstance(rule, basestring) or hasattr(rule, '__call__'):
      self.rules.append((isWhitelist, rule))
    else:
      raise TypeError('Graphite logging rules must be glob pattern or callable. Invalid: %r' % rule)


  def allow(self, rule):
    """Append a whitelisting rule to the chain. The rule is either a function (called
    with the stat name and its value, returns True if it matches), or a Bash-style
    wildcard pattern, such as 'foo.*.bar'."""
    self._addRule(True, rule)


  def forbid(self, rule):
    """Append a blacklisting rule to the chain. The rule is either a function (called
    with the stat name and its value, returns True if it matches), or a Bash-style
    wildcard pattern, such as 'foo.*.bar'."""
    self._addRule(False, rule)
    



class GraphitePeriodicPusher(threading.Thread, GraphitePusher):
  """A thread that periodically pushes all stat values to Graphite."""

  def __init__(self, host, port, prefix, period=60):
    """If prefix is given, it will be prepended to all Graphite
    stats. If it is not given, then a prefix will be derived from the
    hostname."""
    GraphitePusher.__init__(self, host, port, prefix)
    threading.Thread.__init__(self)
    self.daemon = True

    self.period = period


  def run(self):
    """Loop forever, pushing out stats."""
    self.graphite.start()
    while True:
      time.sleep(self.period)
      self.push()


