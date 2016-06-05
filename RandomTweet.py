#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import traceback
import twpy
import dbUtil
import random
from logging import getLogger, FileHandler, Formatter, DEBUG
from tweepy import TweepError


class tw_bot():

    MAX_LOOP_CNT = 20

    def __init__(self, logger=None, list_logger=None):
        self.api = twpy.api
        # logger for log
        self.logger = logger if logger else getLogger(__file__)
        self.logger.setLevel(DEBUG)

        # logger for message list
        self.list_logger = list_logger if list_logger else getLogger('message_list')
        self.list_logger.setLevel(DEBUG)

        # format for log
        formatter = Formatter(fmt='%(asctime)s %(levelname)s  %(message)s',
                              datefmt='%Y/%m/%d %p %I:%M:%S',)

        # handler for log
        self.log_handler = FileHandler(__file__ + '.log', 'a+',
                                       encoding='utf-8')
        self.log_handler.setFormatter(formatter)

        # handler for message list
        self.list_handler = FileHandler(__file__ + '_list.log', 'w',
                                        encoding='utf-8')
        # set handler for log
        self.logger.addHandler(self.log_handler)

        # set handler for message list
        self.list_logger.addHandler(self.list_handler)

        self.con = dbUtil.connect()

    def random_tweet(self):

        random_msgs = dbUtil.getRandomMsgs(self.con)

        count = 0

        while count < tw_bot.MAX_LOOP_CNT:

            random.shuffle(random_msgs)
            msg_json = random_msgs[0]
            msg = msg_json['CONTENTS']
            msg_bytes = msg.encode('utf-8')
            msg = msg_bytes.decode('utf-8')
            msg = msg.strip()

            try:
                (result, status) = self.tweet(msg)
            except (TweepError,  UnicodeEncodeError):
                count += 1
                continue

            self.logger.debug("result: " + str(result))

            if result:

                id = status.id  # ツイートのID
                name = status.author.name  # 名前
                screen_name = status.author.screen_name  # スクリーンネーム
                text = status.text
                dt = status.created_at  # ツイートの日時

                self.logger.info("id: " + str(id))
                self.logger.info("name: " + name)
                self.logger.info("screen_name: " + screen_name)
                self.logger.info("text: " + text)
                self.logger.info("date: " + str(dt))
                self.logger.info("### Tweet OK ###")

                break

            count += 1

        dbUtil.disConnect(self.con)

    def show_all_msgs(self):

        all_msgs = dbUtil.getRandomMsgs(self.con)

        for msg_json in all_msgs:
            no = msg_json['NO']
            msg = msg_json['CONTENTS']
            msg_bytes = msg.encode('utf-8')
            msg = msg_bytes.decode('utf-8')
            msg = msg.strip()

            try:
                self.list_logger.info("no: " + str(no))
                self.list_logger.info("msg: " + str(msg))

            except UnicodeEncodeError:
                raise

        dbUtil.disConnect(self.con)

    def tweet(self, msg):

        result = False
        status = None

        try:
            # tweet
            status = self.api.update_status(status=msg)
            result = True
        except (TweepError, UnicodeEncodeError):
            self.logger.error(traceback.format_exc())
            self.logger.debug("msg: " + msg)
            raise

        return (result, status)

if __name__ == '__main__':

    def usage():
        m = re.split('/', __file__)
        script_name = m[-1]
        print("usage:")
        print("python", script_name, "1 ... random tweet")
        print("                      2 ... dump all messeage list to " + script_name + "_list.log")
        sys.exit()

    param = sys.argv

    if len(param) != 2:
        usage()
    if param[1] != '1' and param[1] != '2':
        usage()

    tw_bot = tw_bot()

    if param[1] == '1':
        tw_bot.random_tweet()
    else:
        tw_bot.show_all_msgs()
