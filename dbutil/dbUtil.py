#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from os.path import sep
import pymysql
from random import choice
from logging import getLogger, StreamHandler, Formatter, INFO

from dbutil.constants import constants
from collections import namedtuple
from dbutil.util.deco import logging
from pit import Pit

logger = getLogger(__file__)
logger.setLevel(INFO)
handler = StreamHandler()
handler.setFormatter(Formatter(fmt='%(levelname)s %(message)s'))
logger.addHandler(handler)


class dbUtil:

    @classmethod
    @logging
    def connect(cls):

        try:

            db_info = Pit.get('db_info')

            host = db_info['host']
            user = db_info['username']
            password = db_info['password']
            db = db_info['db']

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
    def getTwInfo(cls, connection, no):

        fin = None

        try:
            with connection.cursor() as cursor:
                sql_file = path.dirname(path.abspath(__file__)) + sep + constants.SELECT_USER_INFO_SQL
                fin = open(sql_file)
                sql = fin.read()
                cursor.execute(sql, (no,))
                twInfo = cursor.fetchone()
        except Exception:
            raise

        else:
            if twInfo:
                user = twInfo['user']
                con_key = twInfo['consumer_key']
                con_secret = twInfo['consumer_secret']
                token = twInfo['access_token']
                token_secret = twInfo['access_token_secret']

                return (True, [no, user, con_key, con_secret, token, token_secret])
            else:
                return (False, [])
        finally:
            if fin and not fin.closed:
                fin.close()
            else:
                pass

    @classmethod
    @logging
    def getRandomMsgs(cls, connection):

        all_tables = dbUtil.get_all_tables(connection)

        table_name = choice(all_tables)

        try:
            with connection.cursor() as cursor:
                sql_file = path.dirname(path.abspath(__file__)) + sep + constants.SELECT_ALL_MSG_SQL
                fin = open(sql_file)
                sql = fin.read()
                sql = sql.replace('table_name', table_name)
                cursor.execute(sql)
                msgs_jsons = cursor.fetchall()
        except Exception:
            raise
        else:
            if not msgs_jsons:
                return []
            else:
                nos = [msgs_json['NO'] for msgs_json in msgs_jsons]
                msgs = [msgs_json['CONTENTS'] for msgs_json in msgs_jsons]

            return (table_name, nos, msgs)
        finally:
            if fin and not fin.closed:
                fin.close()
            else:
                pass

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
                all_msgs_jsons = cursor.fetchall()
        except Exception:
            raise
        else:
            if not all_msgs_jsons:
                return ()
            else:
                nos = [all_msgs_json['NO'] for all_msgs_json in all_msgs_jsons]
                msgs = [all_msgs_json['CONTENTS'] for all_msgs_json in all_msgs_jsons]
                return (nos, msgs)
        finally:
            if fin and not fin.closed:
                fin.close()
            else:
                pass

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
        except Exception:
            return False
        else:
            # get the ID from the last insert
            return cursor.lastrowid

        finally:
            if fin and not fin.closed:
                fin.close()
            else:
                pass

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
            else:
                pass

    @classmethod
    @logging
    def get_single_msg(cls, connection, table_name, no):

        fin = None

        try:
            with connection.cursor() as cursor:
                sql_file = path.dirname(path.abspath(__file__)) + sep + constants.SELECT_SINGLE_MSG_SQL
                fin = open(sql_file)
                statement = fin.read()
                statement = statement.replace('table_name', table_name)
                cursor.execute(statement, (no,))
                result_json = cursor.fetchone()
                if result_json:
                    msg = result_json['CONTENTS']
                else:
                    msg = ''
        except Exception:
            raise
        else:
            return msg
        finally:
            if fin and not fin.closed:
                fin.close()
            else:
                pass

    @classmethod
    @logging
    def search_msg_by_kword(cls, connection, keyword):

        all_tables = dbUtil.get_all_tables(connection)

        msg_list = []

        fin = None

        try:
            for table_name in all_tables:
                with connection.cursor() as cursor:
                    sql_file = path.dirname(path.abspath(__file__)) + sep + constants.SELECT_MSG_BY_KEWORD_SQL
                    fin = open(sql_file)
                    sql = fin.read()
                    statement = sql.replace('table_name', table_name)
                    cursor.execute(statement, ('%' + keyword + '%',))
                    result_jsons = cursor.fetchall()

                    if result_jsons:
                        nos = [all_result_json['NO'] for all_result_json in result_jsons]
                        msgs = [all_result_json['CONTENTS'] for all_result_json in result_jsons]

                        Result_tuple = namedtuple('Result_tuple', 'nos msgs table_name')
                        result_tuple = Result_tuple(nos, msgs, table_name)

                        msg_list.append(result_tuple)

        except Exception:
            raise

        else:
            return msg_list
        finally:
            if fin and not fin.closed:
                fin.close()
            else:
                pass

    @classmethod
    @logging
    def create_table(cls, connection, table_name):

        fin = None

        try:
            with connection.cursor() as cursor:
                ddl_file = path.dirname(path.abspath(__file__)) + \
                    sep + constants.CREATE_TABLE_DDL
                # connection.begin()
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
            else:
                pass

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
            if fin and not fin.closed:
                fin.close()
            else:
                pass

    @classmethod
    @logging
    def create_database(cls, connection, table_name):

        fin = None

        try:
            with connection.cursor() as cursor:
                ddl_file = path.dirname(path.abspath(__file__)) + sep + constants.CREATE_DATABASE_DDL
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
            else:
                pass

    @classmethod
    @logging
    def drop_database(cls, connection, table_name):

        fin = None

        try:
            with connection.cursor() as cursor:
                ddl_file = path.dirname(path.abspath(__file__)) + sep + constants.DROP_DATABASE_DDL
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
            else:
                pass

    @classmethod
    @logging
    def get_all_tables(cls, connection):

        fin = None

        try:
            with connection.cursor() as cursor:
                sql_file = path.dirname(path.abspath(__file__)) + sep + constants.SELECT_ALL_TABLES_SQL
                fin = open(sql_file)
                sql = fin.read()
                cursor.execute(sql)
                tables = cursor.fetchall()
        except Exception:
            raise

        else:
            if not tables:
                logger.error(constants.SEPARATE_LINE)
                logger.error(constants.NO_TABLE_EXIST_MSG)
                logger.error(constants.SEPARATE_LINE)
                return []
            else:
                all_tables = [table_name_json['table_name'] for table_name_json in tables]
                return all_tables
        finally:
            if fin and not fin.closed:
                fin.close()
            else:
                pass

    @classmethod
    @logging
    def insert_tw_contents(cls,
                           connection,
                           sid,
                           uid,
                           lang,
                           screen_name,
                           name,
                           tweet,
                           reply,
                           created_at):

        fin = None

        try:
            with connection.cursor() as cursor:
                sql_file = path.dirname(path.abspath(__file__)) + \
                    sep + constants.INSERT_TW_CONTENTS_SQL

                fin = open(sql_file)
                statement = fin.read()
                cursor.execute(statement, (sid,
                                           uid,
                                           lang,
                                           screen_name,
                                           name,
                                           tweet,
                                           reply,
                                           created_at))
        except Exception:
            raise
            return False
        else:
            # get the ID from the last insert
            return cursor.lastrowid

        finally:
            if fin and not fin.closed:
                fin.close()
            else:
                pass

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
