# Copyright (c) 2009 Geoffrey Foster. Portions by the Scales Authors.
# 
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.


"""
A Timer implementation that repeats every interval.

Found at http://g-off.net/software/a-python-repeatable-threadingtimer-class

Modified slightly
"""
 
from threading import Event, Thread
 


class RepeatTimer(Thread):
  """A Timer implementation that repeats every interval"""


  def __init__(self, interval, function, iterations=0, args=None, kwargs=None):
    Thread.__init__(self)
    self.interval = interval
    self.function = function
    self.iterations = iterations
    self.args = args or []
    self.kwargs = kwargs or {}
    self.finished = Event()


  def run(self):
    count = 0
    while not self.finished.is_set() and (self.iterations <= 0 or count < self.iterations):
      self.finished.wait(self.interval)
      if not self.finished.is_set():
        self.function(*self.args, **self.kwargs)
        count += 1


  def cancel(self):
    """Stop this thread"""
    self.finished.set()
