# -*- coding: utf-8 -*-

import pymysql.cursors
try:
  import configparser
except ImportError:
  import ConfigParser as configparser

config = configparser.ConfigParser()
#config.sections()

config.read("db_info.ini")

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
    sql = 'SELECT user, ' \
          'consumer_key, ' \
          'consumer_secret, ' \
          'access_token, ' \
          'access_token_secret ' \
          'FROM ' \
          'twitter_users ' \
          'WHERE ' \
          'No = 0';

    cursor.execute(sql)
    result = cursor.fetchone()
    print(result)
finally:
  connection.close()
