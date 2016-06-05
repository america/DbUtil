#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
import traceback
from random import choice
try:
    import configparser
except ImportError:
    import ConfigParser as configparser


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

    sqlFile = "selectUserInfo.sql"

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

    weighted_choices = [("select_msg_from_songs.sql", 1), ("select_msg_from_python.sql", 2), ("select_msg_from_funky.sql", 5)]

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


def disConnect(connection):
    connection.close()
