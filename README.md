scales
======

Scales - Metrics for Python
---------------------------

Tracks server state and statistics, allowing you to see what your server is doing.


### Status

This is a brand new release - issue reports and pull requests are very much appreciated!


### Pre-requisites

scales works best when paired with one of the following web frameworks:

[Flask](http://flask.pocoo.org/)
[Tornado](http://www.tornadoweb.org/)
[Twisted](http://twistedmatrix.com/trac/)


### Installation

    git clone https://github.com/Greplin/scales

    cd scales

    python setup.py install


### Introduction

scales provides you with stats pages so you can see what your server is doing.

It can also send metrics to Graphite for graphing or to a file for crash forensics.

scales is inspired by the fantastic [metrics](https://github.com/codahale/metrics) library, though it is by
no means a port.


#### Simple Use

```python
STATS = scales.collection('/web',
    scales.IntStat('errors'),
    scales.IntStat('success'))

# In a request handler

STATS.success += 1
```


#### Class Stats

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



### Graphite Integration

```python
graphite.GraphitePeriodicPusher('graphite-collector-hostname', 2003, 'my.server.prefix.').start()
```

That's it!  Numeric stats will now be pushed to Graphite every minute.



### Authors

[Greplin, Inc.](http://www.greplin.com)



### License

Copyright 2011 The scales Authors.

Published under The Apache License, see LICENSE
