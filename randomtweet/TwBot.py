#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
import twpy

from dbUtil import dbUtil
from tweepy.streaming import StreamListener
from tweepy import Stream
from datetime import timedelta
from logging import getLogger, StreamHandler, Formatter, DEBUG


class TwListener(StreamListener):
    connection = None

    api = twpy.api

    def __init__(self, logger=None):

        self.logger = logger if logger else getLogger(__file__)
        self.logger.setLevel(DEBUG)
        self.handler = StreamHandler()
        self.handler.setFormatter(Formatter(fmt='%(levelname)s %(message)s'))
        self.logger.addHandler(self.handler)
        self.connection = dbUtil.connect()

    def on_status(self, status):
        self.logger.debug("sid:", status.id)
        self.logger.debug("uid:", status.user.id)
        self.logger.debug("lang:", status.lang)
        self.logger.debug("screen_name:", status.user.screen_name)
        self.logger.debug("name:", status.user.name)
        self.logger.debugi("tweet:", status.text)
        status.created_at += timedelta(hours=9)
        self.logger.debug("time:", status.created_at, "\n")

        created_time = status.created_at
        created_time.strftime('%Y-%m-%d %H:%M:%S')

        result = dbUtil.insert_tw_contents(self.connection,
                                           status.id,
                                           status.user.id,
                                           status.lang,
                                           status.user.screen_name,
                                           status.user.name,
                                           status.text,
                                           0,
                                           status.created_at)
        if result:
            self.connection.commit()
        else:
            self.logger.error('Insert Error!!!')

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    try:
        stream = Stream(twpy.auth, TwListener())

        # get TimeLine
        stream.userstream()
    except KeyboardInterrupt:
        print("動作を停止します")
    except Exception:
        traceback.print_exc()
