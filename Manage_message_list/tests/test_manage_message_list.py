#!/usr/bin/env python
# -*- coding: utf-8 ^*-

import sys
from os.path import dirname
from os.path import sep
from os import pardir
from os import path
from nose.tools import eq_

from DbUtil.dbUtil import dbUtil

pardir_path = dirname(path.abspath(__file__)) + sep + pardir + sep
sys.path.append(pardir_path)
from Manage_message_list.manage_message_list import manage_message_list
from collections import namedtuple
from unittest.mock import patch


class test_manage_message_list():

    conn = None

    def setup(self):
        self.conn = dbUtil.connect()
        dbUtil.create_table(self.conn, 'test_table_for_manage')

    def teardown(self):
        dbUtil.delete_table(self.conn, 'test_table_for_manage')
        dbUtil.disConnect(self.conn)

    def test_insert(self):
        expected = True

        target = manage_message_list()

        Args = namedtuple('Args', 'table_name message')
        args = Args('test_table_for_manage', 'test_message')
        actual = target.insert(args)

        eq_(actual, expected)

    def test_insert_not_exist_table(self):
        expected = False

        target = manage_message_list()

        Args = namedtuple('Args', 'table_name message')
        args = Args('wrong_table_name', 'test_message')
        actual = target.insert(args)

        eq_(actual, expected)

    def test_delete_answer_yes(self):
        expected = True

        target = manage_message_list()

        InsertArgs = namedtuple('InsertArgs', 'table_name message')
        args = InsertArgs('test_table_for_manage', 'test_message')
        target.insert(args)

        DeleteArgs = namedtuple('DeleteArgs', 'table_name no message')
        args = DeleteArgs('test_table_for_manage', [1], 'test_message')
        with patch('builtins.input', return_value='y'):
            actual = target.delete(args)

        eq_(actual, expected)

    def test_delete_answer_no(self):
        expected = False

        target = manage_message_list()

        InsertArgs = namedtuple('InsertArgs', 'table_name message')
        args = InsertArgs('test_table_for_manage', 'test_message')
        target.insert(args)

        DeleteArgs = namedtuple('DeleteArgs', 'table_name no message')
        args = DeleteArgs('test_table_for_manage', [1], 'test_message')
        with patch('builtins.input', return_value='n'):
            actual = target.delete(args)

        eq_(actual, expected)
