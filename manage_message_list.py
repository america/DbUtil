#!/usr/bin/env/python
# -*- coding: utf-8 -*-

import sys
from dbUtil.dbUtil import dbUtil
import traceback
from logging import getLogger, StreamHandler, Formatter, FileHandler, DEBUG
import argparse
from constants import constants
from deco import logging
import pymysql


class manage_message_list():

    @logging
    def __init__(self, logger=None):
        # logger for stdlog
        self.logger = logger if logger else getLogger("log")
        self.logger.setLevel(DEBUG)
        self.handler = StreamHandler()
        self.handler.setFormatter(Formatter(fmt='%(asctime)s %(levelname)s %(message)s',
                                  datefmt='%Y-%m-%d %I:%M:%S',))
        self.logger.addHandler(self.handler)

        self.con = dbUtil.connect()

    @logging
    def insert(self, args):

        table_name = args.table_name
        message = args.message

        if self.exist_table(table_name):
            try:
                no = dbUtil.insert_message(self.con, table_name, message)
                if no:
                    self.con.commit()

                    self.logger.info(constants.SEPARATE_LINE)
                    self.logger.info("'" + message + "'")
                    self.logger.info(constants.INSERT_MSG + table_name + " at No: " + str(no))
                    self.logger.info(constants.SEPARATE_LINE)

            except Exception:
                raise

    @logging
    def delete(self, args):

        table_name = args.table_name
        no_list = args.no

        if self.exist_table(table_name):

            for no in no_list:
                try:
                    msg_json = dbUtil.get_single_msg(self.con, table_name, no)

                    if msg_json:
                        msg = msg_json.get('CONTENTS', constants.NOT_EXIST_MSG)

                        dbUtil.delete_message(self.con, table_name, no)

                        if self.yes_no_input(table_name, no, msg):

                            self.con.commit()
                            self.logger.info(constants.SEPARATE_LINE)
                            self.logger.info("table_name: " + table_name)
                            self.logger.info("no: " + str(no))
                            self.logger.info("msg: " + msg)
                            self.logger.info(constants.DELETE_MSG + table_name)
                            self.logger.info(constants.SEPARATE_LINE)
                    else:
                        self.logger.info(constants.SEPARATE_LINE)
                        self.logger.info(constants.NOT_EXIST_MSG)
                        self.logger.info(constants.SEPARATE_LINE)
                except Exception:
                    raise

    @logging
    def show_all_msgs(self, args):

        table_name = args.table_name

        if self.exist_table(table_name):

            try:
                all_msgs = dbUtil.getAllMsgs(self.con, table_name)

                # logger for message list
                self.list_logger = self.make_filehandler_logger(table_name, 'message_list')

                for msg_json in all_msgs:
                    no = msg_json['NO']
                    msg = msg_json['CONTENTS']

                    self.logger.info(constants.SEPARATE_LINE)
                    self.list_logger.info(constants.SEPARATE_LINE)
                    self.logger.info("no: " + str(no))
                    self.logger.info("msg: " + str(msg))
                    self.list_logger.info("no: " + str(no))
                    self.list_logger.info("msg: " + str(msg))
                    self.logger.info(constants.SEPARATE_LINE)
                    self.list_logger.info(constants.SEPARATE_LINE)
            except Exception:
                raise

    @logging
    def show_all_tables(self, args):

        try:
            all_tables = dbUtil.get_all_tables(self.con)

            self.logger.info(constants.SEPARATE_LINE)
            cnt = 1
            for table_name in all_tables:
                self.logger.info(str(cnt) + ": " + table_name)
                cnt += 1

            self.logger.info(constants.SEPARATE_LINE)

        except Exception:
            raise

    @logging
    def search(self, args):

        keyword = args.keyword

        try:
            result_list = dbUtil.search_msg_by_kword(self.con, keyword)

            # logger for keyword list
            self.list_logger = self.make_filehandler_logger(keyword, 'keyword_list')

            for result_tuple in result_list:
                for json in result_tuple.result_json:
                    self.logger.info(constants.SEPARATE_LINE)
                    self.list_logger.info(constants.SEPARATE_LINE)
                    self.logger.info("table_name: " + result_tuple.table_name)
                    self.list_logger.info("table_name: " + result_tuple.table_name)
                    self.logger.info("no: " + str(json['NO']))
                    self.list_logger.info("no: " + str(json['NO']))
                    self.logger.info("message " + json['CONTENTS'])
                    self.list_logger.info("message " + json['CONTENTS'])
                    self.logger.info(constants.SEPARATE_LINE)
                    self.list_logger.info(constants.SEPARATE_LINE)
        except Exception:
            raise

    @logging
    def create_table(self, args):

        table_name = args.tablename
        try:
            if dbUtil.create_table(self.con, table_name):
                self.logger.info(constants.SEPARATE_LINE)
                self.logger.info(constants.TABLE_CREATED_MSG.replace('table_name', table_name))
                self.logger.info(constants.SEPARATE_LINE)
        except Exception:
            raise

    @logging
    def delete_table(self, args):

        table_name = args.tablename

        if self.exist_table(table_name):
            try:
                if self.yes_no_input(table_name):
                    if dbUtil.delete_table(self.con, table_name):
                        self.logger.info(constants.SEPARATE_LINE)
                        self.logger.info(constants.TABLE_DELETED_MSG.replace('table_name', table_name))
                        self.logger.info(constants.SEPARATE_LINE)
            except Exception:
                raise

    @logging
    def yes_no_input(self, table_name, no=None, msg=None):

        # msg = msg if msg else ''

        self.logger.info(constants.SEPARATE_LINE)
        self.logger.info("table_name: " + table_name)
        if no and msg:
            self.logger.info("no: " + str(no))
            self.logger.info("msg: " + msg)

        while True:
            if no and msg:
                choice = input(constants.CONFIRM_DELETE_MSG_MSG).lower()
            else:
                choice = input(constants.CONFIRM_DELETE_TABLE_MSG).lower()

            if choice in ['y', 'ye', 'yes']:
                return True
            elif choice in ['n', 'no']:
                return False

    @logging
    def exist_table(self, table_name):

        all_tables = [table_name_json['table_name'] for table_name_json in dbUtil.get_all_tables(self.con)]

        if table_name not in all_tables:
            self.logger.error(constants.SEPARATE_LINE)
            self.logger.error(constants.TABLE_NOT_EXIST_MSG.replace('table_name', table_name))
            self.logger.error(constants.SEPARATE_LINE)
            sys.exit(1)

        return True

    @logging
    def make_filehandler_logger(self, handler_prefix, logger_name):

        list_logger = getLogger('keyword_list')
        list_logger.setLevel(DEBUG)
        list_handler = FileHandler(handler_prefix + '_list.log', 'w',
                                   encoding='utf-8')
        list_logger.addHandler(list_handler)

        return list_logger

if __name__ == '__main__':

    def _parse():
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
        parser_delete.add_argument('no', type=int, nargs='*')

        # create the parser for the show_tables command
        parser_show_tables = subparser.add_parser('show_tables', help='show_tables')
        parser_show_tables.set_defaults(func=manager.show_all_tables)

        # create the parser for the search command
        parser_search = subparser.add_parser('search', help='search keyword')
        parser_search.set_defaults(func=manager.search)
        parser_search.add_argument('keyword')

        # create the parser for the create_table command
        parser_create_table = subparser.add_parser('create_table', help='create_table tablename')
        parser_create_table.set_defaults(func=manager.create_table)
        parser_create_table.add_argument('tablename')

        # create the parser for the delete_table command
        parser_create_table = subparser.add_parser('delete_table', help='delete_table tablename')
        parser_create_table.set_defaults(func=manager.delete_table)
        parser_create_table.add_argument('tablename')
        args = parser.parse_args()

        has_func = hasattr(args, 'func')

        if not has_func:
            parser.parse_args(['-h'])
            sys.exit(1)

        return args

    try:
        manager = manage_message_list()
        args = _parse()
        args.func(args)
    except pymysql.InternalError as error:

        (code, message) = error.args

        # table already exists
        if code == 1050:
            manager.logger.error(constants.SEPARATE_LINE)
            manager.logger.error(message)
            manager.logger.error(constants.SEPARATE_LINE)

    except Exception as ex:
        traceback.print_exc()
    finally:
        dbUtil.disConnect(manager.con)
