#!/usr/bin/env python
# -*- coding: utf-8 ^*-

from os import path
from os.path import sep
from os.path import pardir
from nose.tools import eq_, raises, ok_
import pymysql

from dbutil.dbUtil import dbUtil
from dbutil.constants import constants
# from exception import FileNotFoundError


class test_dbUtil():

    conn = None

    def setup(self):
        self.conn = dbUtil.connect()
        dbUtil.create_database(self.conn, 'test_database')
        self.conn.select_db('test_database')
        dbUtil.create_table(self.conn, 'test_table')

    def teardown(self):
        dbUtil.delete_table(self.conn, 'test_table')
        dbUtil.drop_database(self.conn, 'test_database')
        dbUtil.disConnect(self.conn)

    def test_connect(self):
        expected = pymysql.connections.Connection
        _conn = dbUtil.connect()
        ok_(isinstance(_conn, expected))
        dbUtil.disConnect(_conn)

    def test_getTwInfo(self):
        expected = (True, [1, 'user', 'key', 'secret', 'access_token', 'access_token_secret'])
        try:
            with self.conn.cursor() as cursor:
                ddl_file = path.dirname(path.abspath(__file__)) + sep + pardir + sep + constants.CREATE_TW_USER_TABLE_DDL
                fin = open(ddl_file)
                ddl = fin.read()
                cursor.execute(ddl)

                cursor.execute(
                    '''INSERT INTO twitter_users
                       (
                       user,
                       consumer_key,
                       consumer_secret,
                       access_token,
                       access_token_secret
                       )
                       VALUES(
                       'user',
                       'key',
                       'secret',
                       'access_token',
                       'access_token_secret')''')
                self.conn.commit()

        finally:
            if not fin.closed:
                fin.close()

        actual = dbUtil.getTwInfo(self.conn, 1)
        eq_(expected, actual)

    def test_getTwInfo_not_exist(self):
        expected = False
        try:
            with self.conn.cursor() as cursor:
                ddl_file = path.dirname(path.abspath(__file__)) + sep + pardir + sep + constants.CREATE_TW_USER_TABLE_DDL
                fin = open(ddl_file)
                ddl = fin.read()
                cursor.execute(ddl)
        finally:
            if not fin.closed:
                fin.close()

        constants.SELECT_USER_INFO_SQL = 'sql/selectUserInfo_not_exist.sql'
        (result, twInfo) = dbUtil.getTwInfo(self.conn, 99)
        actual = result
        eq_(expected, actual)

    def test_create_table(self):
        expected = True
        actual = dbUtil.create_table(self.conn, 'case_table')
        eq_(actual, expected)
        dbUtil.delete_table(self.conn, 'case_table')

    @raises(pymysql.InternalError)
    def test_create_table_err(self):
        dbUtil.create_table(self.conn, 'test_table')

    def test_insert_message(self):
        expected = ([1], ['test_message'])

        dbUtil.insert_message(self.conn, 'test_table', 'test_message')

        actual = dbUtil.getAllMsgs(self.conn, 'test_table')
        eq_(actual, expected)

    def test_insert_message_rollback01(self):
        expected = ([1], ['test_message'])

        dbUtil.insert_message(self.conn, 'test_table', 'test_message')
        self.conn.commit()

        dbUtil.insert_message(self.conn, 'not_exist_table', 'rollback_message')
        self.conn.rollback()

        actual = dbUtil.getAllMsgs(self.conn, 'test_table')

        eq_(actual, expected)

    def test_insert_message_rollback02(self):
        expected = ()

        dbUtil.insert_message(self.conn, 'test_table', 'test_message')

        dbUtil.insert_message(self.conn, 'not_exist_table', 'rollback_message')
        self.conn.rollback()

        actual = dbUtil.getAllMsgs(self.conn, 'test_table')

        eq_(actual, expected)

    def test_getAllMsgs(self):

        expected = ([1], ['test_message'])
        dbUtil.insert_message(self.conn, 'test_table', 'test_message')
        (no_list, msg_list) = dbUtil.getAllMsgs(self.conn, 'test_table')

        actual = (no_list, msg_list)
        eq_(actual, expected)

    def test_getAllMsgs_not_exist_msg(self):

        expected = ()
        actual = dbUtil.getAllMsgs(self.conn, 'test_table')

        eq_(actual, expected)

    @raises(pymysql.err.ProgrammingError)
    def test_getAllMsgs_err(self):

        dbUtil.getAllMsgs(self.conn, 'not_exist_table')

    def test_getRandomMsgs(self):

        expected = ('test_table', 1, 'test_message')
        dbUtil.insert_message(self.conn, 'test_table', 'test_message')

        constants.SELECT_ALL_TABLES_SQL = 'sql/select_all_tables_one_table.sql'
        (table_name, nos, msgs) = dbUtil.getRandomMsgs(self.conn)

        actual = (table_name, nos[0], msgs[0])
        eq_(actual, expected)

        constants.SELECT_ALL_TABLES_SQL = 'sql/select_all_tables.sql'

    def test_getRandomMsgs_not_exist_msg(self):

        expected = []

        constants.SELECT_ALL_TABLES_SQL = 'sql/select_all_tables_one_table.sql'
        actual = dbUtil.getRandomMsgs(self.conn)

        eq_(actual, expected)

        constants.SELECT_ALL_TABLES_SQL = 'sql/select_all_tables.sql'

    @raises(OSError)
    def test_get_RandomMsgs_err(self):

        try:
            constants.SELECT_ALL_TABLES_SQL = 'no_exists_file'
            dbUtil.getRandomMsgs(self.conn)
        finally:
            constants.SELECT_ALL_TABLES_SQL = "sql/select_all_tables.sql"

    def test_get_single_msg(self):

        expected = 'test_message'
        dbUtil.insert_message(self.conn, 'test_table', 'test_message')

        actual = dbUtil.get_single_msg(self.conn, 'test_table', 1)

        eq_(actual, expected)

    def test_get_single_msg_not_exist_msg(self):

        expected = ''

        actual = dbUtil.get_single_msg(self.conn, 'test_table', 1)

        eq_(actual, expected)

    @raises(pymysql.err.ProgrammingError)
    def test_get_single_msg_err(self):

        dbUtil.get_single_msg(self.conn, 'not_exist_table', 1)

    def test_search_msg_by_kword(self):

        expected = (1, 'test_message', 'test_table',)
        dbUtil.insert_message(self.conn, 'test_table', 'test_message')

        actual = dbUtil.search_msg_by_kword(self.conn, 'test_message')

        eq_((actual[0].nos[0], actual[0].msgs[0], actual[0].table_name), expected)

    def test_get_all_tables(self):

        expected = ['test_table']
        actual = dbUtil.get_all_tables(self.conn)

        eq_(actual, expected)

    def test_get_all_tables_no_table(self):

        expected = []
        constants.SELECT_ALL_TABLES_SQL = 'sql/select_all_tables_no_table.sql'
        actual = dbUtil.get_all_tables(self.conn)

        eq_(actual, expected)

        constants.SELECT_ALL_TABLES_SQL = "sql/select_all_tables.sql"

    @raises(OSError)
    def test_get_all_tables_err(self):

        try:
            constants.SELECT_ALL_TABLES_SQL = 'no_exists_file'
            dbUtil.get_all_tables(self.conn)
        finally:
            constants.SELECT_ALL_TABLES_SQL = "sql/select_all_tables.sql"

    def test_delete_message(self):
        expected = True
        dbUtil.insert_message(self.conn, 'test_table', 'test_message')
        actual = dbUtil.delete_message(self.conn, 'test_table', 1)
        eq_(actual, expected)

    def test_delete_message_not_exist_message(self):
        expected = False
        actual = dbUtil.delete_message(self.conn, 'test_table', 2)
        eq_(actual, expected)

    @raises(OSError)
    def test_delete_message_err(self):

        try:
            constants.DELETE_MSG_SQL = 'no_exists_file'
            dbUtil.delete_message(self.conn, 'test_table', 1)
        finally:
            constants.DELETE_MSG_SQL = "sql/delete_msg.sql"

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

    def test_diconnecti_err(self):
        _conn = dbUtil.connect()
        dbUtil.disConnect(_conn)
        dbUtil.disConnect(_conn)
