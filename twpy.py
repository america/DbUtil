#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dbUtil import dbUtil
import tweepy
from deco import logging


class twpy:

    @logging
    def __init___(self):
        pass

    @logging
    def main(self):
        self.con = dbUtil.connect()

        twitterInfo = dbUtil.getTwInfo(self.con)

        CONSUMER_KEY = twitterInfo["consumer_key"]
        CONSUMER_SECRET = twitterInfo["consumer_secret"]

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

        ACCESS_TOKEN = twitterInfo["access_token"]
        ACCESS_SECRET = twitterInfo["access_token_secret"]

        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

        # APIインスタンスを作成
        api = tweepy.API(auth)

        dbUtil.disConnect(self.con)

        return api

twpy = twpy()

api = twpy.main()
