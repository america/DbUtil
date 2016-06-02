#!/usr/bin/env/python
# -*- coding: utf-8 -*-

import sys
import dbUtil
import traceback


class insert_python_tips():

    def __init__(self):
        pass

    def insert(self, data):

        result = False

        sqlFile = "insert_python_tips.sql"

        con = dbUtil.connect()

        try:
            with con.cursor() as cursor:
                statement = open(sqlFile).read()
                statement = statement.strip()
                result = cursor.execute(statement, (data,))
        except (Exception,):
            raise

        con.commit()

        if result:
            dbUtil.disConnect()

            print("Insert OK")


if __name__ == '__main__':

    param = sys.argv

    if len(param) < 2:
        print("This script is required only one argument.")
        sys.exit()

    data = param[1]

    try:
        insert_python_tips = insert_python_tips()
        insert_python_tips.insert(data)
    except Exception:
        traceback.print_exc()
