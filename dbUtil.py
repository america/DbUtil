#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
import traceback
from random import choice
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

DB_INFO_INI = "db_info.ini"
select_user_info_sql = "sql/selectUserInfo.sql"
select_single_msg_sql = "sql/select_single_msg.sql"
select_all_msg_sql = "sql/select_all.sql"
insert_msg_sql = "sql/insert.sql"
delete_msg_sql = "sql/delete.sql"
select_all_tales_sql = "sql/select_all_tables.sql"


def connect():

    config = configparser.ConfigParser()

    config.read(DB_INFO_INI)

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
    return connection


def getTwInfo(connection):

    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = open(select_user_info_sql).read()
            cursor.execute(sql)
            twInfo = cursor.fetchone()
            return twInfo
    except Exception:
        traceback.print_exc()


def getRandomMsgs(connection):

    all_tables = [table_name_json['table_name'] for table_name_json in get_all_tables(connection)]

    weighted_choices = [(all_tables[3], 3),
                        (all_tables[2], 2),
                        (all_tables[0], 1),
                        (all_tables[1], 2)]

    population = [val for val, cnt in weighted_choices for i in range(cnt)]

    table_name = choice(population)

    try:
        with connection.cursor() as cursor:
            sql = open(select_all_msg_sql).read()
            sql = sql.replace('table_name', table_name)
            cursor.execute(sql)
            msgs = cursor.fetchall()
            return msgs
    except Exception:
        traceback.print_exc()


def getAllMsgs(connection, table_name):

    try:
        with connection.cursor() as cursor:
            sql = open(select_all_msg_sql).read()
            sql = sql.replace('table_name', table_name)
            cursor.execute(sql)
            msgs = cursor.fetchall()
    except BaseException:
        raise

    return msgs


def insert_message(connection, table_name, message):

    try:
        with connection.cursor() as cursor:
            statement = open(insert_msg_sql).read()
            statement = statement.replace('table_name', table_name)
            result = cursor.execute(statement, (message,))
            return result
    except BaseException:
        raise


def get_single_msg(connection, table_name, no):

    try:
        with connection.cursor() as cursor:
            statement = open(select_single_msg_sql).read()
            statement = statement.replace('table_name', table_name)
            cursor.execute(statement, (no,))
            msg = cursor.fetchone()
    except Exception:
        traceback.print_exc()
        raise

    return msg


def get_all_tables(connection):

    try:
        with connection.cursor() as cursor:
            sql = open(select_all_tales_sql).read()
            cursor.execute(sql)
            tables = cursor.fetchall()
    except BaseException:
        raise

    return tables


def disConnect(connection):
    connection.close()
