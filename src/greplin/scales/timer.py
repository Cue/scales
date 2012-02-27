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

Modified to remove the Event signal as we never intend to cancel it.
This was done primarily for compatibility with libraries like gevent
"""

from thread import start_new_thread
from time import sleep


def RepeatTimer(interval, function, iterations=0, args=None, kwargs=None):
    def __repeat_timer(interval, function, iterations=0, args=None, kwargs=None):
        interval = interval
        function = function
        iterations = iterations
        args = args or []
        kwargs = kwargs or {}

        count = 0
        while iterations <= 0 or count < iterations:
            sleep(interval)
            function(*args, **kwargs)
            count += 1

    ident = start_new_thread(__repeat_timer, (interval, function, iterations, args, kwargs))
    return ident
