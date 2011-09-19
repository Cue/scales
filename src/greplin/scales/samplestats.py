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

"""Sample statistics. Based on the Java code in Yammer metrics."""

import random
from math import sqrt, floor



class UniformSample(object):
  """A uniform sample of values over time."""

  def __init__(self):
    """Create an empty sample."""
    self.sample = [0.0] * 1028
    self.count = 0
    self.min = float('inf')
    self.max = float('-inf')


  def clear(self):
    """Clear the sample."""
    for i in range(len(self.sample)):
      self.sample[i] = 0.0
    self.count = 0


  def __len__(self):
    """Number of samples stored."""
    return min(len(self.sample), self.count)


  def update(self, value):
    """Add a value to the sample."""
    self.count += 1
    c = self.count
    if c < len(self.sample):
      self.sample[c-1] = value
    else:
      r = random.randint(0, c)
      if r < len(self.sample):
        self.sample[r] = value

    self.min = min(self.min, value)
    self.max = max(self.max, value)


  def __iter__(self):
    """Return an iterator of the values in the sample."""
    return iter(self.sample[:len(self)])


  @property
  def mean(self):
    """Return the sample mean."""
    if len(self) == 0:
      return float('NaN')
    arr = self.sample[:len(self)]
    return sum(arr) / float(len(arr))


  @property
  def stddev(self):
    """Return the sample standard deviation."""
    if len(self) < 2:
      return float('NaN')
    # The stupidest algorithm, but it works fine.
    arr = self.sample[:len(self)]
    mean = sum(arr) / len(arr)
    bigsum = 0.0
    for x in arr:
      bigsum += (x - mean)**2
    return sqrt(bigsum / (len(arr) - 1))


  def percentiles(self, percentiles):
    """Given a list of percentiles (floats between 0 and 1), return a
    list of the values at those percentiles, interpolating if
    necessary."""
    try:
      scores = [0.0]*len(percentiles)

      if self.count > 0:
        values = self.sample[:len(self)]
        values.sort()

        for i in range(len(percentiles)):
          p = percentiles[i]
          pos = p * (len(values) + 1)
          if pos < 1:
            scores[i] = values[0]
          elif pos > len(values):
            scores[i] = values[-1]
          else:
            upper, lower = values[int(pos - 1)], values[int(pos)]
            scores[i] = lower + (pos - floor(pos)) * (upper - lower)

      return scores
    except IndexError:
      return [float('NaN')] * len(percentiles)
