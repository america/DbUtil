#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dbutil.dbUtil import dbUtil
import tweepy
from dbutil.util.deco import logging


class twpy:

    @logging
    def __init___(self):
        pass

    @logging
    def main(self):
        self.con = dbUtil.connect()

        (reslut, twitterInfo) = dbUtil.getTwInfo(self.con, 0)

        CONSUMER_KEY = twitterInfo[2]
        CONSUMER_SECRET = twitterInfo[3]

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

        ACCESS_TOKEN = twitterInfo[4]
        ACCESS_SECRET = twitterInfo[5]

        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

        # APIインスタンスを作成
        api = tweepy.API(auth)

        dbUtil.disConnect(self.con)

        return (api, auth)

twpy = twpy()

(api, auth) = twpy.main()
