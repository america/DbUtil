#!/usr/bin/env python
# -*- coding: utf-8 ^*-

import sys
from os.path import dirname
from os.path import sep
from os import pardir
from os import path
from nose.tools import eq_
# import pymysql

from DbUtil.dbUtil import dbUtil
pardir_path = dirname(path.abspath(__file__)) + sep + pardir + sep
sys.path.append(pardir_path)
from constants import constants
# from Manage_message_list import manage_message_list
import subprocess

from logging import getLogger, StreamHandler, Formatter, DEBUG


logger = getLogger(__file__)
logger.setLevel(DEBUG)
handler = StreamHandler()
handler.setFormatter(Formatter(fmt='%(levelname)s %(message)s'))
logger.addHandler(handler)


class test_manage_message_list():

    conn = None

    args = ['which', 'python3']
    subproc_args = {'stdin': subprocess.PIPE,
                    'stdout': subprocess.PIPE,
                    'stderr': subprocess.STDOUT,
                    'close_fds': True,
                    }
    p = subprocess.Popen(args, **subproc_args)

    (stdouterr, stdin) = (p.stdout, p.stdin)

    python_cmd = stdouterr.readline().decode('utf-8').rstrip()

    logger.debug(constants.SEPARATE_LINE)
    logger.debug('python_cmd: ' + python_cmd)
    logger.debug(constants.SEPARATE_LINE)

    def setup(self):
        self.conn = dbUtil.connect()
        dbUtil.create_table(self.conn, 'test_table')

    def teardown(self):
        dbUtil.delete_table(self.conn, 'test_table')
        dbUtil.disConnect(self.conn)

    def test_insert(self):
        expected = 0
        cmd = self.python_cmd + " " + pardir_path + "manage_message_list.py insert test_table test_message"
        logger.debug(constants.SEPARATE_LINE)
        logger.debug('cmd: ' + cmd)
        logger.debug(constants.SEPARATE_LINE)

        args = cmd.strip().split(" ")
        subproc_args = {'stdin': subprocess.PIPE,
                        'stdout': subprocess.PIPE,
                        'stderr': subprocess.STDOUT,
                        'close_fds': True,
                        }
        _p = subprocess.Popen(args, **subproc_args)

        (stdouterr, stdin) = (_p.stdout, _p.stdin)

        if sys.version_info.major == 3:
            while True:
                line = stdouterr.readline().decode('utf-8')
                if not line:
                    break
                logger.debug(line.rstrip())
        else:
            while True:
                line = stdouterr.readline()
                if not line:
                    break
                logger.debug(line.rstrip())

        actual = _p.wait()
        logger.debug(constants.SEPARATE_LINE)
        logger.debug(actual)
        logger.debug(constants.SEPARATE_LINE)
        eq_(actual, expected)
