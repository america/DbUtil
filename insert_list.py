#!/usr/bin/env/python
# -*- coding: utf-8 -*-

import sys
import dbUtil
import traceback
from logging import getLogger, StreamHandler, FileHandler, DEBUG
import re


class insert_list():

    def __init__(self, logger=None, list_logger=None):
        # logger for log
        self.logger = logger if logger else getLogger("log")
        self.logger.setLevel(DEBUG)
        handler = StreamHandler()
        self.logger.addHandler(handler)

        # logger for message list
        self.list_logger = list_logger if list_logger else getLogger('message_list')
        self.list_logger.setLevel(DEBUG)
        list_handler = FileHandler(__file__ + '_list.log', 'w',
                                   encoding='utf-8')
        self.list_logger.addHandler(list_handler)

        self.con = dbUtil.connect()

    def insert(self, data):

        result = False

        sqlFile = "insert_list.sql"

        try:
            with self.con.cursor() as cursor:
                statement = open(sqlFile).read()
                statement = statement.strip()
                result = cursor.execute(statement, (data,))
        except (Exception,):
            raise

        self.con.commit()

        dbUtil.disConnect(self.con)

        if result:

            self.logger.info("Insert OK")

    def show_all_msgs(self):

        sql_file = "select_msg_from_funky.sql"
        try:
            all_msgs = dbUtil.getAllMsgs(self.con, sql_file)

            for msg_json in all_msgs:
                no = msg_json['NO']
                msg = msg_json['CONTENTS']

                self.list_logger.info("no: " + str(no))
                self.list_logger.info("msg: " + str(msg))

        except Exception:
            traceback.print_exc()
        dbUtil.disConnect(self.con)

if __name__ == '__main__':

    def usage():
        m = re.split('/', __file__)
        script_name = m[-1]
        print("usage:")
        print("python", script_name, "1 [wanna insert message] ... insert msg to message list")
        print("                      2 [free word]            ... dump all messeage list to " + script_name + "_list.log")
        sys.exit()

    param = sys.argv

    if len(param) != 3:
        usage()

    if param[1] != '1' and param[1] != '2':
        usage()

    data = param[2]

    try:
        insert_list = insert_list()

        if param[1] == '1':
            insert_list.insert(data)
        else:
            insert_list.show_all_msgs()

    except Exception:
        traceback.print_exc()
