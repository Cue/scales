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

"""Defines a Cyclone request handler for status reporting.

Install like:
  handlers=[
    ...
    (r'/stats/(.*)', StatsHandler, {'serverName': 'my_app_name'}),
  ]

"""


from greplin.scales import tornadolike

import cyclone.web


class StatsHandler(tornadolike.Handler, cyclone.web.RequestHandler):
  """Cyclone request handler for a status page."""
