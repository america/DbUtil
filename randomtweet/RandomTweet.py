#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
import twpy

from dbutil.dbUtil import dbUtil
from random import choice
from logging import getLogger, \
    StreamHandler, \
    FileHandler, \
    Formatter, \
    DEBUG, \
    INFO
from dbutil.constants import constants
from dbutil.util.deco import logging


class RandomTweet():

    file_logger = None

    @logging
    def __init__(self):
        self.api = twpy.api

        # logger for log
        self.file_logger = \
            self.file_logger if self.file_logger else getLogger(__file__)
        self.file_logger.setLevel(DEBUG)

        # format for log
        formatter = Formatter(fmt='%(asctime)s %(levelname)s  %(message)s',
                              datefmt='%Y/%m/%d %p %I:%M:%S',)

        # handler for log
        self.log_handler = FileHandler(__file__ + '.log', 'a+',
                                       encoding='utf-8')
        self.log_handler.setFormatter(formatter)

        # set handler for log
        self.file_logger.addHandler(self.log_handler)

        try:
            self.con = dbUtil.connect()
        except Exception:
            raise

    @logging
    def random_tweet(self):

        (table_name, no_list, msg_list) = dbUtil.getRandomMsgs(self.con)

        count = 0

        while count < constants.TWEET_MAX_LOOP_CNT:

            msg = choice(msg_list)
            index = msg_list.index(msg)
            no = no_list[index]
            msg = msg.strip()

            try:
                (result, status) = self.tweet(table_name, no, msg)

                if result:
                    break

            except Exception:
                count += 1
                continue
            else:
                count += 1

        dbUtil.disConnect(self.con)

    @logging
    def tweet(self, table_name, no, msg):

        stdlogger = getLogger('std')
        stdlogger.setLevel(INFO)
        stdlogger.addHandler(StreamHandler())

        result = False
        try:
            if constants.TWEET_FLAG:
                # tweet
                status = self.api.update_status(status=msg)

                if status:
                    id = status.id  # ID
                    name = status.author.name  # name
                    screen_name = status.author.screen_name  # screen_name
                    text = status.text  # a content you tweet
                    dt = status.created_at  # date at tweet

                    self.file_logger.info("id: " + str(id))
                    self.file_logger.info("name: " + name)
                    self.file_logger.info("screen_name: " + screen_name)
                    self.file_logger.info("text: " + text)
                    self.file_logger.info("date: " + str(dt))
                    self.file_logger.info("### Tweet OK ###")

                    stdlogger.info("id: " + str(id))
                    stdlogger.info("name: " + name)
                    stdlogger.info("screen_name: " + screen_name)
                    stdlogger.info("text: " + text)
                    stdlogger.info("date: " + str(dt))
                    stdlogger.info("### Tweet OK ###")
            else:

                stdlogger.info(constants.SEPARATE_LINE)
                stdlogger.info('table_name: ' + table_name)
                stdlogger.info('no: ' + str(no))
                status = stdlogger.info('message: ' + msg)

            result = True
        except Exception:
            self.file_logger.error(traceback.format_exc())
            self.file_logger.error("msg: " + msg)
            raise

        else:
            return (result, status)

if __name__ == '__main__':

    try:
        rt = RandomTweet()
        rt.random_tweet()
    except Exception:
        traceback.print_exc()
