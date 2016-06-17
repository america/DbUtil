#!/usr/bin/env/python
# -*- coding: utf-8 -*-

TWEET_FLAG = False

# file name
DB_INFO_INI = "db_info.ini"
SELECT_USER_INFO_SQL = "sql/selectUserInfo.sql"
SELECT_SINGLE_MSG_SQL = "sql/select_single_msg.sql"
SELECT_ALL_MSG_SQL = "sql/select_all_msg.sql"
INSERT_MSG_SQL = "sql/insert_msg.sql"
DELETE_MSG_SQL = "sql/delete_msg.sql"
SELECT_ALL_TABLES_SQL = "sql/select_all_tables.sql"
# SELECT_ALL_TABLES_SQL = "sql/select_all_tables_test.sql"

# message
SEPARATE_LINE = "--------------------"
NOT_EXIST_MSG = "This no doesn't exist."
INSERT_MSG = "This message was inserted in "
DELETE_MSG = "This message was deleted from "
CONFIRM_MSG = "Are you sure to delete this message? [y/N]: "
TABLE_NOT_EXIST_MSG = "Table is called [ table_name ] doesn't exist."
DB_INFO_INI_NOT_EXIST_MSG = DB_INFO_INI + " does't exist."
NO_TABLE_EXIST_MSG = "No table exists."
DB_CONNECTION_ESTABLISHED_MSG = "DB Connection established."
DB_CONNECTION_RELEASED_MSG = "DB Connection released."
