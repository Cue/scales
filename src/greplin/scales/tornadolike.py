from greplin import scales
from greplin.scales import formats, util


class Handler(object):

  serverName = None


  def initialize(self, serverName): # pylint: disable=W0221
    """Initializes the handler."""
    self.serverName = serverName


  def get(self, path): # pylint: disable=W0221
    """Renders a GET request, by showing this nodes stats and children."""
    path = path or ''
    path = path.lstrip('/')
    parts = path.split('/')
    if not parts[0]:
      parts = parts[1:]
    statDict = util.lookup(scales.getStats(), parts)

    if statDict is None:
      self.set_status(404)
      self.finish('Path not found.')
      return

    outputFormat = self.get_argument('format', default='html')
    query = self.get_argument('query', default=None)
    if outputFormat == 'json':
      formats.jsonFormat(self, statDict, query)
    elif outputFormat == 'prettyjson':
      formats.jsonFormat(self, statDict, query, pretty=True)
    else:
      formats.htmlHeader(self, '/' + path, self.serverName, query)
      formats.htmlFormat(self, tuple(parts), statDict, query)

    return None
