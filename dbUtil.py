#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
import traceback
from random import choice
try:
    import configparser
except ImportError:
    import ConfigParser as configparser


select_single_msg_sql = "sql/select_single_msg.sql"


def connect():
    iniFile = "db_info.ini"

    config = configparser.ConfigParser()

    config.read(iniFile)

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

    sqlFile = "sql/selectUserInfo.sql"

    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = open(sqlFile).read()
            cursor.execute(sql)
            twInfo = cursor.fetchone()
            return twInfo
    except BaseException:
        traceback.print_exc()


def getRandomMsgs(connection):

    weighted_choices = [("sql/select_msg_from_songs.sql", 3),
                        ("sql/select_msg_from_python.sql", 2),
                        ("sql/select_msg_from_funky.sql", 1),
                        ("sql/select_msg_from_precepts.sql", 2)]

    population = [val for val, cnt in weighted_choices for i in range(cnt)]

    sql_file = choice(population)

    try:
        with connection.cursor() as cursor:
            sql = open(sql_file).read()
            cursor.execute(sql)
            msgs = cursor.fetchall()
            return msgs
    except BaseException:
        traceback.print_exc()


def getAllMsgs(connection, sql_file):

    try:
        with connection.cursor() as cursor:
            sql = open(sql_file).read()
            cursor.execute(sql)
            msgs = cursor.fetchall()
            return msgs
    except BaseException:
        traceback.print_exc()


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


def disConnect(connection):
    connection.close()
