# Copyright 2015 Google Inc
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import calendar
import datetime
import unittest
import mock
import time

from google.appengine.api import memcache
from google.appengine.ext import testbed


class MemcacheTestCase(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()
        
    @mock.patch('time.time')
    def testMemcache(self, time_mock):
    	initial_datetime = datetime.datetime(year=2018, month=7, day=5, hour=9, minute=1, second=0)
    	time_mock.return_value = time.mktime(initial_datetime.timetuple())
    	
    	day_after = datetime.datetime(year=2018, month=7, day=6, hour=9, minute=1, second=0)
    	memcache.set('TEST_K', 1, time=calendar.timegm(day_after.timetuple()))
    	self.assertEqual(memcache.get('TEST_K'), 1)
        
    @mock.patch('time.time')
    def testMemcacheExpiration(self, time_mock):
    	initial_datetime = datetime.datetime(year=2018, month=7, day=1, hour=9, minute=1, second=0)
    	time_mock.return_value = time.mktime(initial_datetime.timetuple())
    	#mock.patch('time.time', mock.MagicMock(return_value=time.mktime(initial_datetime.timetuple())))
    	
    	day_after = datetime.datetime(year=2018, month=7, day=2, hour=9, minute=0, second=0)
    	memcache.set('TEST_K', 1, time=calendar.timegm(day_after.timetuple()))
    	self.assertEqual(memcache.get('TEST_K'), 1)
    	
    	day_after_after = datetime.datetime(year=2018, month=7, day=3, hour=9, minute=1, second=0)
    	time_mock.return_value = time.mktime(day_after_after.timetuple())
    	#mock.patch('time.time', mock.MagicMock(return_value=time.mktime(day_after_tomorrow.timetuple())))
    	
    	self.assertIsNone(memcache.get('TEST_K'))



if __name__ == '__main__':
    unittest.main()
