#!/usr/bin/env python
# -*- coding: utf-8 ^*-

import unittest
from dbUtil import dbUtil
import pymysql


class test_dbUtil(unittest.TestCase):

    def setUp(self):
        self.conn = dbUtil.connect()

    def tearDown(self):
        dbUtil.disConnect(self.conn)

    def test_connect001(self):
        expected = pymysql.connections.Connection
        actual = dbUtil.connect()
        self.assertIsInstance(actual, expected)

    def test_create_table001(self):
        expected = True
        actual = dbUtil.create_table(self.conn, 'test_table')
        self.assertEqual(actual, expected)

    def test_delete_table001(self):
        expected = True
        actual = dbUtil.delete_table(self.conn, 'test_table')
        self.assertEqual(actual, expected)

    def test_disConnect001(self):
        expected = True
        actual = dbUtil.disConnect(self.conn)
        self.assertEqual(actual, expected)

if __name__ == '__main__':

    unittest.main()
