#!/usr/bin/env/python
# -*- coding: utf-8 -*-

import sys
import dbUtil
import traceback
from logging import getLogger, StreamHandler, DEBUG


class insert_songs():

    def __init__(self, logger=None):
        self.logger = logger if logger else getLogger("log")
        self.logger.setLevel(DEBUG)
        handler = StreamHandler()
        self.logger.addHandler(handler)

    def insert(self, data):

        result = False

        sqlFile = "insert_songs.sql"

        con = dbUtil.connect()

        try:
            with con.cursor() as cursor:
                statement = open(sqlFile).read()
                statement = statement.strip()
                result = cursor.execute(statement, (data,))
        except (Exception,):
            raise

        con.commit()

        dbUtil.disConnect(con)

        if result:

            self.logger.info("Insert OK")


if __name__ == '__main__':

    param = sys.argv

    if len(param) != 2:
        print("This script is required only one argument.")
        sys.exit()

    data = param[1]

    try:
        insert_songs = insert_songs()
        insert_songs.insert(data)
    except Exception:
        traceback.print_exc()
