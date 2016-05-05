#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
import re

from tweepy.streaming import StreamListener
from tweepy import Stream

from twpy import *

class TwListener(StreamListener):
  def on_status(self, status):
    print("ID:", status.id)
    print("Lang:", status.lang)
    print("ScreenName:", status.user.screen_name)
    print("Name:", status.user.name)
    print("Tweet:", status.text)
    print("Time:", status.created_at,"\n")

    return True

  def on_error(self, status):
    print(status)

if __name__ == '__main__':
  try:
    stream = Stream(auth, TwListener())

    # get TimeLine
    stream.userstream()
  except KeyboardInterrupt:
    print("動作を停止します")
  except Exception as e:
    traceback.print_exc()
