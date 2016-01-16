#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
try:
  import configparser
except ImportError:
  import ConfigParser as configparser

iniFile = "db_info.ini"
sqlFile = "selectUserInfo.sql"

config = configparser.ConfigParser()
#config.sections()

config.read(iniFile)

host     = config['info']['host']
user     = config['info']['user']
password = config['info']['password']
db       = config['info']['db']

# Connect to the database
connection = pymysql.connect(host=host,
                             user=user,
                             password=password,
                             db=db,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
  with connection.cursor() as cursor:
    # Read a single record
    sql = open(sqlFile).read()
    cursor.execute(sql)
    result = cursor.fetchone()
    print(result)
finally:
  cursor.close()
  connection.close()
