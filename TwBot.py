#!/usr/bin/env python
# -*- coding: utf-8 -*-

import twpy
import dbUtil
import random
import traceback

from tweepy.streaming import StreamListener
from tweepy import Stream

class TwListener(StreamListener):
  def on_data(self, daga)
    if data.startwith("{"):
      print data
    return True

  def on_error(self, status):
    print status

if __name__ == '__main__'
  stream = Stream(auth, TwListener())

  # get TimeLine
  stream.userstream()
