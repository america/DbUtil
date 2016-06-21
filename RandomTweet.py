#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
import twpy
from dbUtil import dbUtil
from random import choice
from logging import getLogger, StreamHandler, FileHandler, Formatter, DEBUG
from tweepy import TweepError
import constants


class tw_bot():

    def __init__(self, logger=None, list_logger=None):
        self.api = twpy.api
        # logger for log
        self.logger = logger if logger else getLogger(__file__)
        self.logger.setLevel(DEBUG)

        # format for log
        formatter = Formatter(fmt='%(asctime)s %(levelname)s  %(message)s',
                              datefmt='%Y/%m/%d %p %I:%M:%S',)

        # handler for log
        self.log_handler = FileHandler(__file__ + '.log', 'a+',
                                       encoding='utf-8')
        self.log_handler.setFormatter(formatter)

        # set handler for log
        self.logger.addHandler(self.log_handler)

        try:
            self.con = dbUtil.connect()
        except Exception:
            raise

    def random_tweet(self):

        (table_name, random_msgs) = dbUtil.getRandomMsgs(self.con)

        count = 0

        while count < constants.TWEET_MAX_LOOP_CNT:

            msg_json = choice(random_msgs)
            no = msg_json['NO']
            msg = msg_json['CONTENTS']
            msg_bytes = msg.encode('utf-8')
            msg = msg_bytes.decode('utf-8')
            msg = msg.strip()

            try:
                (result, status) = self.tweet(table_name, no, msg)
            except (TweepError,  UnicodeEncodeError):
                count += 1
                continue

            if result:
                if status:
                    id = status.id  # ID
                    name = status.author.name  # name
                    screen_name = status.author.screen_name  # screen_name
                    text = status.text  # a content you tweet
                    dt = status.created_at  # date at tweet

                    self.logger.info("id: " + str(id))
                    self.logger.info("name: " + name)
                    self.logger.info("screen_name: " + screen_name)
                    self.logger.info("text: " + text)
                    self.logger.info("date: " + str(dt))
                    self.logger.info("### Tweet OK ###")

                break

            count += 1

        dbUtil.disConnect(self.con)

    def tweet(self, table_name, no, msg):

        try:
            if constants.TWEET_FLAG:
                # tweet
                status = self.api.update_status(status=msg)
            else:
                stdlogger = getLogger('std')
                stdlogger.setLevel(DEBUG)
                stdlogger.addHandler(StreamHandler())

                stdlogger.info(constants.SEPARATE_LINE)
                stdlogger.info('table_name: ' + table_name)
                stdlogger.info('no: ' + str(no))
                status = stdlogger.info('message: ' + msg)

            result = True
        except (TweepError, UnicodeEncodeError):
            self.logger.error(traceback.format_exc())
            self.logger.debug("msg: " + msg)
            raise

        return (result, status)

if __name__ == '__main__':

    try:
        tw_bot = tw_bot()
        tw_bot.random_tweet()
    except Exception:
        traceback.print_exc()
