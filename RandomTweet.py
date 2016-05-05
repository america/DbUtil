#!/usr/bin/env python
# -*- coding: utf-8 -*-

import twpy
import dbUtil
import random
import traceback

class TwBot():

  def __init__(self):
    self.api = twpy.api

  def randomTweet(self):
    con = dbUtil.connect()
    randomMsgs = dbUtil.getRandomMsgs(con)

    random.shuffle(randomMsgs)
    msg = randomMsgs[0]

    try:
      #tweet
      self.api.update_status(status=msg['CONTENTS']);
    except:
      traceback.print_exc()
    finally:
      dbUtil.disConnect(con)

if __name__ == '__main__':

  twBot = TwBot()
  twBot.randomTweet()
