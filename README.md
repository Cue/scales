Scales - Metrics for Python
===========================

Tracks server state and statistics, allowing you to see what your server is
doing. It can also send metrics to Graphite for graphing or to a file for crash forensics. 

scales is inspired by the fantastic [metrics](https://github.com/codahale/metrics) library, though it is by
no means a port.

This is a brand new release - issue reports and pull requests are very much appreciated!



### Installation

    git clone https://github.com/Greplin/scales

    cd scales

    python setup.py install

The HTTP statistics viewer in scales requires one of the following web frameworks:

[Flask](http://flask.pocoo.org/)

[Tornado](http://www.tornadoweb.org/)

[Twisted](http://twistedmatrix.com/trac/)

If you aren't sure, go with Flask; it's compatible with most every other event
loop. You can get it with `pip install flask`.


### How to use it

Getting started and adding stats only takes a few lines of code:

```python
from greplin import scales

STATS = scales.collection('/web',
    scales.IntStat('errors'),
    scales.IntStat('success'))

# In a request handler

STATS.success += 1
```

This code will collect two integer stats, which is nice, but what you really
want to do is *look* at those stats, to get insight into what your server is
doing. There are two main ways of doing this: the HTTP server and Graphite
logging.

The HTTP server is the simplest way to get stats out of a running server. The
easiest way, if you have Flask installed, is to do this:

```python
import greplin.scales.flaskhandler as statserver
statserver.serveInBackground(8765, serverName='something-server-42')
```

This will spawn a background thread that will listen on port 8765, and serve up
a very convenient view of all your stats. To see it, go to

http://localhost:8765/status/

You can also get the stats in JSON by appending `?format=json` to the URL.

The HTTP server is good for doing spot checks on the internals of running
servers, but what about continuous monitoring? How do you generate graphs of
stats over time? This is where [Graphite](http://graphite.wikidot.com/) comes
in. Graphite is a server for collecting stats and graphing them, and scales has
easy support for using it. Again, this is handled in a background thread:

```python
graphite.GraphitePeriodicPusher('graphite-collector-hostname', 2003, 'my.server.prefix.').start()
```

That's it!  Numeric stats will now be pushed to Graphite every minute. You can
exclude stats from graphite logging with the `doNotLog(prefix)` method of the
`GraphitePeriodicPusher` class.

#### Timing sections of code

To better understand the performance of certain critical sections of your code,
scales lets you collect timing information:

```python
from greplin import scales

STATS = scales.collection('/web',
    scales.IntStat('errors'),
    scales.IntStat('success'),
    scales.PmfStat('latency'))

# In a request handler

with STATS.latency.time():
  do_something_expensive()
```

This will collect statistics on the running times of that section of code: mean
time, median, standard deviation, and several percentiles to help you locate
outlier times. This happens in pretty small constant memory, so don't worry
about the cost; time anything you like.

You can gather this same kind of sample statistics about any quantity. Just make
a `PmfStat` and assign new values to it:

```python
for person in people:
  person.perturb(42)
  STATS.wistfulness = person.getFeelings('wistfulness')
```


#### Class Stats

While global stats are easy to use, sometimes making stats class-based makes
more sense. This is supported; just make sure to give each instance of the class
a unique identifier with `scales.init`.

```python
class Handler(object):

  success = scales.IntStat('requests')
  latency = scales.PmfStat('latency')

  def __init__(self):
    scales.init(self, '/handler')


  def handleRequest(self, request):
    self.requests += 1
    with self.latency.time():
      doSomething()
```


#### Gauges

Simple lambdas can be used to generate stat values.

```python
STATS = scales.collection(scales.Stat('currentTime', lambda: time.time())
```

Of course this works with arbitrary function objects, so the example above could
also be written:

```python
STATS = scales.collection(scales.Stat('currentTime', time.time)
```


#### Hierarchical Stats + Aggregation

Stats can inherit their path from the object that creates them, and (non-gauge) stats can be aggregated up to ancestors.

```python
class Processor(object):
  """Example processing management object."""

  threadStates = scales.HistogramAggregationStat('state')
  finished = scales.SumAggregationStat('finished')

  def __init__(self):
    scales.init(self, '/processor')
    self.threads = 0


  def createThread(self):
    threadId = self.threads
    self.threads += 1
    SomeThread(threadId).start()



class SomeThread(object):
  """Stub of a processing thread object."""

  state = scales.Stat('state')
  finished = scales.IntStat('finished')


  def __init__(self, threadId):
    scales.initChild(self, 'thread-%d' % threadId)


  def processingLoop(self):
    while True:
      self.state = 'waitingForTask'
      getTask()
      self.state = 'performingTask'
      doTask()
      self.finished += 1

```

This will result in stats at paths like `/processor/thread-0/started` as well as stats like
`/processor/state/waitingForTask` which counts the number of threads in the `waitingForTask` state.




### Authors

[Greplin, Inc.](http://www.greplin.com)



### License

Copyright 2011 The scales Authors.

Published under The Apache License, see LICENSE
