
from cStringIO import StringIO

from greplin import scales
from greplin.scales import formats, util

from bottle import abort, request, run, Bottle
import functools

def bottlestats(server_name, path=''):
    """Renders a GET request, by showing this nodes stats and children."""
    path = path.lstrip('/')
    parts = path.split('/')
    if not parts[0]:
        parts = parts[:1]
    stat_dict = util.lookup(scales.getStats(), parts)

    if stat_dict is None:
        abort(404, "Not Found")
        return

    output = StringIO()
    output_format = request.query.get('format', 'html')
    query = request.query.get('query', None)
    if output_format == 'json':
        formats.jsonFormat(output, stat_dict, query)
    elif output_format == 'prettyjson':
        formats.jsonFormat(output, stat_dict, query, pretty=True)
    else:
        formats.htmlHeader(output, '/' + path, server_name, query)
        formats.htmlFormat(output, tuple(parts), stat_dict, query)

    return output.getvalue()

def register_stats_handler(app, server_name, prefix='/_stats/'):
    """Register the stats handler with a Flask app, serving routes
    with a given prefix. The prefix defaults to '/_stats/', which is
    generally what you want."""
    if not prefix.endswith('/'):
        prefix += '/'
    handler = functools.partial(bottlestats, server_name)

    app.get(prefix, callback=handler)
    app.get(prefix + '<path:path>', callback=handler)


