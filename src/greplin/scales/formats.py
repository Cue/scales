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

"""Formatting methods for stats."""

from greplin import scales

import cgi
try:
  # Prefer simplejson for speed.
  import simplejson as json
except ImportError:
  import json
import operator
import re

OPERATORS = {
  '>=': operator.ge,
  '>': operator.gt,
  '<=': operator.lt,
  '<': operator.le,
  '=': operator.eq,
  '==': operator.eq,
  '!=': operator.ne
}

OPERATOR = re.compile('(%s)' % '|'.join(OPERATORS.keys()))


def runQuery(statDict, query):
  """Filters for the given query."""
  parts = [x.strip() for x in OPERATOR.split(query)]
  assert len(parts) in (1, 3)
  queryKey = parts[0]

  result = {}
  for key, value in statDict.items():
    if key == queryKey:
      if len(parts) == 3:
        op = OPERATORS[parts[1]]
        try:
          queryValue = type(value)(parts[2]) if value else parts[2]
        except (TypeError, ValueError):
          continue
        if not op(value, queryValue):
          continue
      result[key] = value
    elif isinstance(value, scales.StatContainer) or isinstance(value, dict):
      child = runQuery(value, query)
      if child:
        result[key] = child
  return result


def htmlHeader(output, path, serverName, query = None):
  """Writes an HTML header."""
  if path and path != '/':
    output.write('<title>%s - Status: %s</title>' % (serverName, path))
  else:
    output.write('<title>%s - Status</title>' % serverName)
  output.write('''
<style>
body,td { font-family: monospace }
.level div {
  padding-bottom: 4px;
}
.level .level {
  margin-left: 2em;
  padding: 1px 0;
}
span { color: #090; vertical-align: top }
.key { color: black; font-weight: bold }
.int, .float { color: #00c }
</style>
  ''')
  output.write('<h1 style="margin: 0">Stats</h1>')
  output.write('<h3 style="margin: 3px 0 18px">%s</h3>' % serverName)
  output.write(
      '<p><form action="#" method="GET">Filter: <input type="text" name="query" size="20" value="%s"></form></p>' %
      (query or ''))


def htmlFormat(output, pathParts = (), statDict = None, query = None):
  """Formats as HTML, writing to the given object."""
  statDict = statDict or scales.getStats()
  if query:
    statDict = runQuery(statDict, query)
  _htmlRenderDict(pathParts, statDict, output)


def _htmlRenderDict(pathParts, statDict, output):
  """Render a dictionary as a table - recursing as necessary."""
  keys = statDict.keys()
  keys.sort()

  links = []

  output.write('<div class="level">')
  for key in keys:
    keyStr = cgi.escape(str(key))
    value = statDict[key]
    if hasattr(value, '__call__'):
      value = value()
    if hasattr(value, 'keys'):
      valuePath = pathParts + (keyStr,)
      if isinstance(value, scales.StatContainer) and value.isCollapsed():
        link = '/status/' + '/'.join(valuePath)
        links.append('<div class="key"><a href="%s">%s</a></div>' % (link, keyStr))
      else:
        output.write('<div class="key">%s</div>' % keyStr)
        _htmlRenderDict(valuePath, value, output)
    else:
      output.write('<div><span class="key">%s</span> <span class="%s">%s</span></div>' %
                   (keyStr, type(value).__name__, cgi.escape(str(value)).replace('\n', '<br>')))

  if links:
    for link in links:
      output.write(link)

  output.write('</div>')


def jsonFormat(output, statDict = None, query = None, pretty = False):
  """Formats as JSON, writing to the given object."""
  statDict = statDict or scales.getStats()
  if query:
    statDict = runQuery(statDict, query)
  indent = (pretty and 2) or None
  json.dump(statDict, output, cls=scales.StatContainerEncoder, indent=indent)
  output.write('\n')
