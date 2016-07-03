#!/usr/bin/env python
# -*- coding: utf-8 ^*-

from nose.tools import eq_, raises
import pymysql

from dbUtil.dbUtil import dbUtil
from constants import constants


class test_dbUtil():

    conn = None

    def setup(self):
        self.conn = dbUtil.connect()
        dbUtil.create_table(self.conn, 'test_table')

    def teardown(self):
        dbUtil.delete_table(self.conn, 'test_table')
        dbUtil.disConnect(self.conn)

    def test_connect(self):
        expected = pymysql.connections.Connection
        _conn = dbUtil.connect()
        assert isinstance(_conn, expected)
        dbUtil.disConnect(_conn)

    @raises(IOError)
    def test_connect_err(self):
        constants.DB_INFO_INI = 'not_exist_file'
        try:
            dbUtil.connect()
        finally:
            constants.DB_INFO_INI = 'db_info.ini'

    # @with_setup(setup_func, teardown_func)
    def test_create_table(self):
        expected = True
        actual = dbUtil.create_table(self.conn, 'case_table')
        eq_(actual, expected)
        dbUtil.delete_table(self.conn, 'case_table')

    # @with_setup(setup_func, teardown_func)
    def test_insert_message(self):
        expected = 1

        actual = dbUtil.insert_message(self.conn, 'test_table', 'test_message')

        eq_(actual, expected)

    # @with_setup(setup_func, teardown_func)
    def test_getAllMsgs(self):

        expected = (1, 'test_message')
        dbUtil.insert_message(self.conn, 'test_table', 'test_message')
        result_json = dbUtil.getAllMsgs(self.conn, 'test_table')

        actual = (result_json[0]['NO'], result_json[0]['CONTENTS'])

        eq_(actual, expected)

    # @with_setup(setup_func, teardown_func)
    def test_delete_message(self):
        expected = True
        dbUtil.insert_message(self.conn, 'test_table', 'test_message')
        actual = dbUtil.delete_message(self.conn, 'test_table', 1)
        eq_(actual, expected)

    # @with_setup(setup_func, teardown_func)
    def test_delete_message_err(self):
        expected = False
        actual = dbUtil.delete_message(self.conn, 'test_table', 2)
        eq_(actual, expected)

    # @with_setup(setup_func, teardown_func)
    def test_delete_table(self):
        expected = True
        dbUtil.create_table(self.conn, 'test_table_for_delete_table')
        actual = dbUtil.delete_table(self.conn, 'test_table_for_delete_table')
        eq_(actual, expected)

    def test_diconnect(self):
        expected = True
        conn = dbUtil.connect()
        actual = dbUtil.disConnect(conn)
        eq_(actual, expected)
