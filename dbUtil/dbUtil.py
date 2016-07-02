#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from os.path import sep
from os import pardir
import sys
import pymysql
from random import choice
from logging import getLogger, StreamHandler, Formatter, INFO
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

pardir_path = path.dirname(path.abspath(__file__)) + sep + pardir
sys.path.append(pardir_path)
from constants import constants
from collections import namedtuple
from deco import logging

logger = getLogger(__file__)
logger.setLevel(INFO)
handler = StreamHandler()
handler.setFormatter(Formatter(fmt='%(asctime)s %(levelname)s %(message)s',
                               datefmt='%Y-%m-%d %I:%M:%S',))
logger.addHandler(handler)


class dbUtil:

    @classmethod
    @logging
    def connect(cls):

        config = configparser.ConfigParser()

        db_info_ini = path.dirname(path.abspath(__file__)) + sep + constants.DB_INFO_INI

        try:
            if not path.exists(db_info_ini):
                raise IOError(constants.DB_INFO_INI_NOT_EXIST_MSG)
            else:
                config.read(db_info_ini)

                host = config['info']['host']
                user = config['info']['user']
                password = config['info']['password']
                db = config['info']['db']

                # Connect to the database
                connection = pymysql.connect(host=host,
                                             user=user,
                                             password=password,
                                             db=db,
                                             charset='utf8mb4',
                                             cursorclass=pymysql.cursors.DictCursor)

                connection.autocommit(False)

                logger.debug(constants.SEPARATE_LINE)
                logger.debug(constants.DB_CONNECTION_ESTABLISHED_MSG)
                logger.debug(constants.SEPARATE_LINE)
        except IOError:
            raise
        except Exception:
            raise
        else:
            return connection

    @classmethod
    @logging
    def getTwInfo(cls, connection):

        try:
            with connection.cursor() as cursor:
                # Read a single record
                sql = open(constants.SELECT_USER_INFO_SQL).read()
                cursor.execute(sql)
                twInfo = cursor.fetchone()
        except Exception:
            raise

        else:
            return twInfo

    @classmethod
    @logging
    def getRandomMsgs(cls, connection):

        all_tables = [table_name_json['table_name'] for table_name_json in dbUtil.get_all_tables(connection)]

        table_name = choice(all_tables)

        try:
            with connection.cursor() as cursor:
                sql = open(constants.SELECT_ALL_MSG_SQL).read()
                sql = sql.replace('table_name', table_name)
                cursor.execute(sql)
                msgs = cursor.fetchall()
                return (table_name, msgs)
        except Exception:
            raise

    @classmethod
    @logging
    def getAllMsgs(cls, connection, table_name):

        try:
            with connection.cursor() as cursor:
                sql_file = path.dirname(path.abspath(__file__)) + sep + constants.SELECT_ALL_MSG_SQL
                fin = open(sql_file)
                sql = fin.read()
                sql = sql.replace('table_name', table_name)
                cursor.execute(sql)
                msgs = cursor.fetchall()
        except BaseException:
            raise
        else:
            return msgs
        finally:
            if fin and not fin.closed:
                fin.close()

    @classmethod
    @logging
    def insert_message(cls, connection, table_name, message):

        fin = None

        try:
            with connection.cursor() as cursor:
                sql_file = path.dirname(path.abspath(__file__)) + sep + constants.INSERT_MSG_SQL
                fin = open(sql_file)
                statement = fin.read()
                statement = statement.replace('table_name', table_name)
                cursor.execute(statement, (message,))
                connection.commit()
        except Exception:
            raise
        else:
            # get the ID from the last insert
            return cursor.lastrowid

        finally:
            if fin and not fin.closed:
                fin.close()

    @classmethod
    @logging
    def delete_message(cls, connection, table_name, no):

        fin = None

        try:
            with connection.cursor() as cursor:
                sql_file = path.dirname(path.abspath(__file__)) + sep + constants.DELETE_MSG_SQL
                fin = open(sql_file)
                statement = fin.read()
                statement = statement.replace('table_name', table_name)
                statement = statement.strip()
                result = cursor.execute(statement, (no,))
                connection.commit()
        except Exception:
            raise
        else:
            if result:
                return True
            else:
                return False
        finally:
            if fin and not fin.closed:
                fin.close()

    @classmethod
    @logging
    def get_single_msg(cls, connection, table_name, no):

        try:
            with connection.cursor() as cursor:
                statement = open(constants.SELECT_SINGLE_MSG_SQL).read()
                statement = statement.replace('table_name', table_name)
                cursor.execute(statement, (no,))
                msg = cursor.fetchone()
        except Exception:
            raise

        return msg

    @classmethod
    @logging
    def search_msg_by_kword(cls, connection, keyword):

        all_tables = [table_name_json['table_name'] for table_name_json in dbUtil.get_all_tables(connection)]

        msg_list = []

        try:
            for table_name in all_tables:
                with connection.cursor() as cursor:
                    sql = open(constants.SELECT_MSG_BY_KEWORD_SQL).read()
                    statement = sql.replace('table_name', table_name)
                    cursor.execute(statement, ('%' + keyword + '%',))
                    results = cursor.fetchall()
                    Result_tuple = namedtuple('Result_tuple', 'result_json table_name')
                    result_tuple = Result_tuple(results, table_name)
                    msg_list.append(result_tuple)

        except Exception:
            raise

        return msg_list

    @classmethod
    @logging
    def create_table(cls, connection, table_name):

        fin = None

        try:
            with connection.cursor() as cursor:
                ddl_file = path.dirname(path.abspath(__file__)) + sep + constants.CREATE_TABLE_DDL
                fin = open(ddl_file)
                ddl = fin.read()
                ddl = ddl.replace('table_name', table_name)
                cursor.execute(ddl)
                connection.commit()
        except Exception:
            raise

        else:
            return True

        finally:
            if fin and not fin.closed:
                fin.close()

    @classmethod
    @logging
    def delete_table(cls, connection, table_name):

        fin = None

        try:
            with connection.cursor() as cursor:
                ddl_file = path.dirname(path.abspath(__file__)) + sep + constants.DROP_TABLE_DDL
                fin = open(ddl_file)
                ddl = fin.read()
                ddl = ddl.replace('table_name', table_name)
                cursor.execute(ddl)
                connection.commit()
        except Exception:
            raise

        else:
            return True

        finally:
            if not fin.closed:
                fin.close()

    @classmethod
    @logging
    def get_all_tables(cls, connection):

        try:
            with connection.cursor() as cursor:
                sql = open(constants.SELECT_ALL_TABLES_SQL).read()
                cursor.execute(sql)
                tables = cursor.fetchall()
        except Exception:
            raise

        if not tables:
            logger.info(constants.SEPARATE_LINE)
            logger.error(constants.NO_TABLE_EXIST_MSG)
            dbUtil.disConnect(connection)
            sys.exit(1)

        return tables

    @classmethod
    @logging
    def disConnect(cls, connection):
        try:
            if connection.open:
                logger.debug(constants.SEPARATE_LINE)
                connection.close()
                logger.debug(constants.DB_CONNECTION_RELEASED_MSG)
                logger.debug(constants.SEPARATE_LINE)
        except Exception:
            raise
        else:
            return True
