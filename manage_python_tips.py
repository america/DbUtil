#!/usr/bin/env/python
# -*- coding: utf-8 -*-

import sys
import dbUtil
import traceback
from logging import getLogger, StreamHandler, FileHandler, DEBUG
import re


class manage_python_tips():

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

        sqlFile = "sql/insert_python_tips.sql"

        con = dbUtil.connect()

        try:
            with con.cursor() as cursor:
                statement = open(sqlFile).read()
                statement = statement.strip()
                result = cursor.execute(statement, (data,))
        except (Exception,):
            raise

        con.commit()

        dbUtil.disConnect(con)

        if result:

            self.logger.info("Insert OK")

    def delete(self, table_name, no):

        sqlFile = "sql/delete.sql"

        con = dbUtil.connect()

        msg_json = dbUtil.get_single_msg(con, table_name, no)

        msg = msg_json['CONTENTS']

        try:
            with con.cursor() as cursor:
                statement = open(sqlFile).read()
                statement = statement.replace('table_name', table_name)
                statement = statement.strip()
                cursor.execute(statement, (no,))
        except (Exception,):
            raise

        if self.yes_no_input(msg):
            con.commit()

            dbUtil.disConnect(con)

            self.logger.info("delete OK")

    def show_all_msgs(self):

        sql_file = "sql/select_msg_from_python.sql"

        try:
            all_msgs = dbUtil.getAllMsgs(self.con, sql_file)

            for msg_json in all_msgs:
                no = msg_json['NO']
                msg = msg_json['CONTENTS']

                self.list_logger.info("no: " + str(no))
                self.list_logger.info("msg: " + str(msg))
        except Exception:
            raise

        dbUtil.disConnect(self.con)

    def yes_no_input(self, msg):

        self.logger.info("msg: " + msg)

        while True:
            choice = input('Are you sure to delete this message [y/N]: ')

            if choice in ['y', 'ye', 'yes']:
                return True
            elif choice in ['n', 'no']:
                return False


if __name__ == '__main__':

    def usage():
        m = re.split('/', __file__)
        script_name = m[-1]
        print("usage:")
        print("python", script_name, "1 [table name] [wanna insert message] ... insert msg to message list")
        print("                      2 [free word]                         ... dump all messeages to " + script_name + "_list.log")
        sys.exit()

    param = sys.argv

    if len(param) != 4:
        usage()

    if param[1] != '1' and param[1] != '2' and param[1] != '3':
        usage()

    table_name = param[2]
    data = param[3]
    no = param[3]

    try:
        manager = manage_python_tips()

        if param[1] == '1':
            manager.insert(data)
        elif param[1] == '2':
            manager.show_all_msgs()
        else:
            manager.delete(table_name, no)

    except Exception:
        traceback.print_exc()
