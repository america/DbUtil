#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pymysql
from random import choice
from logging import getLogger, StreamHandler,  DEBUG
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
    def inner(*args, **kwargs):
        logger.info(__name__ + '#' + func.__name__)

        result = func(*args, **kwargs)
        return result
    return inner


def connect():

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


def getTwInfo(connection):

    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = open(constants.SELECT_USER_INFO_SQL).read()
            cursor.execute(sql)
            twInfo = cursor.fetchone()
            return twInfo
    except Exception:
        raise


def getRandomMsgs(connection):

    all_tables = [table_name_json['table_name'] for table_name_json in get_all_tables(connection)]

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


def getAllMsgs(connection, table_name):

    try:
        with connection.cursor() as cursor:
            sql = open(constants.SELECT_ALL_MSG_SQL).read()
            sql = sql.replace('table_name', table_name)
            cursor.execute(sql)
            msgs = cursor.fetchall()
    except BaseException:
        raise

    return msgs


def insert_message(connection, table_name, message):

    try:
        with connection.cursor() as cursor:
            statement = open(constants.INSERT_MSG_SQL).read()
            statement = statement.replace('table_name', table_name)
            cursor.execute(statement, (message,))
            # get the ID from the last insert
            return cursor.lastrowid
    except Exception:
        raise


def delete_message(connection, table_name, no):

    try:
        with connection.cursor() as cursor:
            statement = open(constants.DELETE_MSG_SQL).read()
            statement = statement.replace('table_name', table_name)
            statement = statement.strip()
            return cursor.execute(statement, (no,))
    except Exception:
        raise


def get_single_msg(connection, table_name, no):

    try:
        with connection.cursor() as cursor:
            statement = open(constants.SELECT_SINGLE_MSG_SQL).read()
            statement = statement.replace('table_name', table_name)
            cursor.execute(statement, (no,))
            msg = cursor.fetchone()
    except Exception:
        raise

    return msg


def search_msg_by_kword(connection, keyword):

    all_tables = [table_name_json['table_name'] for table_name_json in get_all_tables(connection)]

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


def get_all_tables(connection):

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
        disConnect(connection)
        sys.exit(1)

    return tables


def disConnect(connection):
    if connection.open:
        logger.debug(constants.SEPARATE_LINE)
        connection.close()
        logger.debug(constants.DB_CONNECTION_RELEASED_MSG)
