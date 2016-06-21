#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pymysql
from random import choice
from logging import getLogger, StreamHandler, Formatter, DEBUG
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
import constants
from collections import namedtuple


logger = getLogger(__file__)
logger.setLevel(DEBUG)
handler = StreamHandler()
logger.addHandler(handler)


def logging(func):
    "Decorator"
    def wrapper(obj, *args, **kwargs):
        handler.setFormatter(Formatter(fmt='%(asctime)s %(levelname)s %(message)s',
                                       datefmt='%Y-%m-%d %I:%M:%S',))
        logger.debug(func.__qualname__ + " START")

        result = func(obj, *args, **kwargs)

        logger.debug(func.__qualname__ + " END")
        return result
    return wrapper


class dbUtil:

    @classmethod
    @logging
    def connect(cls):

        config = configparser.ConfigParser()

        try:
            if not os.path.exists(constants.DB_INFO_INI):
                logger.error(constants.SEPARATE_LINE)
                logger.error(constants.DB_INFO_INI_NOT_EXIST_MSG)
                sys.exit(1)

            config.read(constants.DB_INFO_INI)

            host = config['info']['host']
            user = config['info']['user']
            password = config['info']['password']
            db = config['info']['db']

            # Connect to the database
            connection = pymysql.connect(host=host,
                                         user=user,
                                         password=password,
                                         db=db,
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)

            logger.debug(constants.SEPARATE_LINE)
            logger.debug(constants.DB_CONNECTION_ESTABLISHED_MSG)
            return connection
        except Exception:
            raise

    @classmethod
    def getTwInfo(cls, connection):

        try:
            with connection.cursor() as cursor:
                # Read a single record
                sql = open(constants.SELECT_USER_INFO_SQL).read()
                cursor.execute(sql)
                twInfo = cursor.fetchone()
                return twInfo
        except Exception:
            raise

    @classmethod
    def getRandomMsgs(cls, connection):

        all_tables = [table_name_json['table_name'] for table_name_json in dbUtil.get_all_tables(connection)]

        table_name = choice(all_tables)

        try:
            with connection.cursor() as cursor:
                sql = open(constants.SELECT_ALL_MSG_SQL).read()
                sql = sql.replace('table_name', table_name)
                cursor.execute(sql)
                msgs = cursor.fetchall()
                return (table_name, msgs)
        except Exception:
            raise

    @classmethod
    def getAllMsgs(cls, connection, table_name):

        try:
            with connection.cursor() as cursor:
                sql = open(constants.SELECT_ALL_MSG_SQL).read()
                sql = sql.replace('table_name', table_name)
                cursor.execute(sql)
                msgs = cursor.fetchall()
        except BaseException:
            raise

        return msgs

    @classmethod
    def insert_message(cls, connection, table_name, message):

        try:
            with connection.cursor() as cursor:
                statement = open(constants.INSERT_MSG_SQL).read()
                statement = statement.replace('table_name', table_name)
                cursor.execute(statement, (message,))
                # get the ID from the last insert
                return cursor.lastrowid
        except Exception:
            raise

    @classmethod
    def delete_message(cls, connection, table_name, no):

        try:
            with connection.cursor() as cursor:
                statement = open(constants.DELETE_MSG_SQL).read()
                statement = statement.replace('table_name', table_name)
                statement = statement.strip()
                return cursor.execute(statement, (no,))
        except Exception:
            raise

    @classmethod
    def get_single_msg(cls, connection, table_name, no):

        try:
            with connection.cursor() as cursor:
                statement = open(constants.SELECT_SINGLE_MSG_SQL).read()
                statement = statement.replace('table_name', table_name)
                cursor.execute(statement, (no,))
                msg = cursor.fetchone()
        except Exception:
            raise

        return msg

    @classmethod
    def search_msg_by_kword(cls, connection, keyword):

        all_tables = [table_name_json['table_name'] for table_name_json in dbUtil.get_all_tables(connection)]

        msg_list = []

        try:
            for table_name in all_tables:
                with connection.cursor() as cursor:
                    sql = open(constants.SELECT_MSG_BY_KEWORD_SQL).read()
                    statement = sql.replace('table_name', table_name)
                    cursor.execute(statement, ('%' + keyword + '%',))
                    results = cursor.fetchall()
                    Result_tuple = namedtuple('Result_tuple', 'result_json table_name')
                    result_tuple = Result_tuple(results, table_name)
                    msg_list.append(result_tuple)

        except Exception:
            raise

        return msg_list

    @classmethod
    def get_all_tables(cls, connection):

        try:
            with connection.cursor() as cursor:
                sql = open(constants.SELECT_ALL_TABLES_SQL).read()
                cursor.execute(sql)
                tables = cursor.fetchall()
        except Exception:
            raise

        if not tables:
            logger.info(constants.SEPARATE_LINE)
            logger.error(constants.NO_TABLE_EXIST_MSG)
            dbUtil.disConnect(connection)
            sys.exit(1)

        return tables

    @classmethod
    def disConnect(cls, connection):
        if connection.open:
            logger.debug(constants.SEPARATE_LINE)
            connection.close()
            logger.debug(constants.DB_CONNECTION_RELEASED_MSG)
