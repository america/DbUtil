#!/usr/bin/env/python
# -*- coding: utf-8 -*-

import sys
import dbUtil
import traceback
from logging import getLogger, StreamHandler, FileHandler, DEBUG
import argparse


class manage_message_list():

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

    def insert(self, args):

        table_name = args.table_name
        message = args.message

        result = False

        try:
            result = dbUtil.insert_message(self.con, table_name, message)
        except (Exception,):
            raise

        self.con.commit()

        dbUtil.disConnect(self.con)

        if result:

            self.logger.info("Insert OK")

    def delete(self, args):

        table_name = args.table_name
        no = args.no

        msg = "This no is empty message."
        result = False

        sqlFile = "sql/delete.sql"

        msg_json = dbUtil.get_single_msg(self.con, table_name, no)

        if msg_json:
            msg = msg_json.get('CONTENTS', 'This no is empty message.')

        try:
            with self.con.cursor() as cursor:
                statement = open(sqlFile).read()
                statement = statement.replace('table_name', table_name)
                statement = statement.strip()
                result = cursor.execute(statement, (no,))
        except (Exception,):
            raise

        if not result:
            self.logger.info(msg)
        elif self.yes_no_input(msg):

            self.con.commit()

            dbUtil.disConnect(self.con)

            self.logger.info("delete OK")

    def show_all_msgs(self, args):

        table_name = args.table_name

        try:
            all_msgs = dbUtil.getAllMsgs(self.con, table_name)

            for msg_json in all_msgs:
                no = msg_json['NO']
                msg = msg_json['CONTENTS']

                self.list_logger.info("no: " + str(no))
                self.list_logger.info("msg: " + str(msg))
        except Exception:
            raise

        dbUtil.disConnect(self.con)

    def yes_no_input(self, msg):

        msg = msg if msg else ''
        self.logger.info("msg: " + msg)

        while True:
            choice = input('Are you sure to delete this message [y/N]: ').lower()

            if choice in ['y', 'ye', 'yes']:
                return True
            elif choice in ['n', 'no']:
                return False


if __name__ == '__main__':

    manager = manage_message_list()

    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(help='sub-command help')

    # create the parser for the insert command
    parser_insert = subparser.add_parser('insert', help='insert table_name massage')
    parser_insert.set_defaults(func=manager.insert)
    parser_insert.add_argument('table_name')
    parser_insert.add_argument('message')

    # create the parser for the show command
    parser_show = subparser.add_parser('show', help='show table_name ')
    parser_show.set_defaults(func=manager.show_all_msgs)
    parser_show.add_argument('table_name')

    # create the parser for the delete command
    parser_delete = subparser.add_parser('delete', help='delete table_name no')
    parser_delete.set_defaults(func=manager.delete)
    parser_delete.add_argument('table_name')
    parser_delete.add_argument('no', type=int)

    args = parser.parse_args()

    has_func = hasattr(args, 'func')

    if not has_func:
        parser.parse_args(['-h'])
        sys.exit(1)

    try:
        args.func(args)
    except Exception:
        traceback.print_exc()
