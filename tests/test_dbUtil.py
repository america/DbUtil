#!/usr/bin/env python
# -*- coding: utf-8 ^*-

import sys
from os.path import sep
from os import pardir
from os import getcwd
try:
    import unittest2 as unittest
except (ImportError):
    import unittest
import pymysql

pardir_path = getcwd() + sep + pardir
sys.path.append(pardir_path)

from dbUtil import dbUtil


class test_dbUtil(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # cls.conn = dbUtil.connect()
        pass

    def setUp(self):
        self.conn = dbUtil.connect()
        dbUtil.create_table(self.conn, 'test_table')

    def tearDown(self):
        dbUtil.delete_table(self.conn, 'test_table')
        dbUtil.disConnect(self.conn)

    @classmethod
    def tearDownClass(cls):
        # dbUtil.disConnect(cls.conn)
        pass

    def test_connect(self):
        expected = pymysql.connections.Connection
        self.assertIsInstance(self.conn, expected)

    def test_create_table(self):
        expected = True

        actual = dbUtil.create_table(self.conn, 'case_table')

        self.assertEqual(actual, expected)

        dbUtil.delete_table(self.conn, 'case_table')

    def test_insert_message(self):
        expected = 1

        actual = dbUtil.insert_message(self.conn, 'test_table', 'test_message')

        self.assertEqual(actual, expected)

    def test_getAllMsgs(self):

        expected = (1, 'test_message')
        dbUtil.insert_message(self.conn, 'test_table', 'test_message')
        result_json = dbUtil.getAllMsgs(self.conn, 'test_table')

        actual = (result_json[0]['NO'], result_json[0]['CONTENTS'])

        self.assertEqual(actual, expected)

    def test_delete_message(self):
        expected = True
        dbUtil.insert_message(self.conn, 'test_table', 'test_message')

        actual = dbUtil.delete_message(self.conn, 'test_table', 1)

        # actual = dbUtil.delete_message(self.conn, 'test_table', 2)
        self.assertEqual(actual, expected)

    def test_delete_table(self):
        expected = True

        dbUtil.create_table(self.conn, 'test_table_for_delete_table')
        actual = dbUtil.delete_table(self.conn, 'test_table_for_delete_table')

        self.assertEqual(actual, expected)

    def test_disConnect(self):
        expected = True
        _connection = dbUtil.connect()

        actual = dbUtil.disConnect(_connection)

        self.assertEqual(actual, expected)

if __name__ == '__main__':

    unittest.main()
