#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
import twpy
# import re

from dbUtil import dbUtil
from tweepy.streaming import StreamListener
from tweepy import Stream
from datetime import timedelta


class TwListener(StreamListener):
    connection = None

    api = twpy.api

    def __init__(self):
        self.connection = dbUtil.connect()

    def on_status(self, status):
        print("sid:", status.id)
        print("uid:", status.user.id)
        print("lang:", status.lang)
        print("screen_name:", status.user.screen_name)
        print("name:", status.user.name)
        print("tweet:", status.text)
        status.created_at += timedelta(hours=9)
        print("time:", status.created_at, "\n")

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
            print('Insert Error!!!')

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
