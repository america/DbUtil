#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
import traceback
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

    sqlFile = "selectRandomMsg.sql"

    try:
        with connection.cursor() as cursor:

            sql = open(sqlFile).read()
            cursor.execute(sql)
            msgs = cursor.fetchall()
            return msgs
    except BaseException:
        traceback.print_exc()


def disConnect(connection):
    connection.close()
