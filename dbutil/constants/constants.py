#!/usr/bin/env/python
# -*- coding: utf-8 -*-

# try to tweet max frequency
TWEET_MAX_LOOP_CNT = 20

# the flag of tweet or stdout
TWEET_FLAG = True

# file name
DB_INFO_INI = "db_info.ini"
SELECT_USER_INFO_SQL = "sql/selectUserInfo.sql"
SELECT_SINGLE_MSG_SQL = "sql/select_single_msg.sql"
SELECT_ALL_MSG_SQL = "sql/select_all_msg.sql"
INSERT_MSG_SQL = "sql/insert_msg.sql"
DELETE_MSG_SQL = "sql/delete_msg.sql"
SELECT_ALL_TABLES_SQL = "sql/select_all_tables.sql"
SELECT_MSG_BY_KEWORD_SQL = "sql/select_msg_by_keyword.sql"
CREATE_TABLE_DDL = "sql/create_table.ddl"
CREATE_TW_USER_TABLE_DDL = "sql/create_tw_user_table.ddl"
DROP_TABLE_DDL = "sql/drop_table.ddl"
CREATE_DATABASE_DDL = "sql/create_database.ddl"
DROP_DATABASE_DDL = "sql/drop_database.ddl"
INSERT_TW_CONTENTS_SQL = "sql/insert_tw_contents.sql"

# message
SEPARATE_LINE = "-" * 80
NOT_EXIST_MSG = "This No doesn't exist."
INSERT_MSG = "This message was inserted in "
DELETE_MSG = "This message was deleted from "
CONFIRM_DELETE_MSG_MSG = "Are you sure to delete this message? [y/N]: "
CONFIRM_DELETE_TABLE_MSG = "Are you sure to delete this table? [y/N]: "
TABLE_NOT_EXIST_MSG = "The table [ table_name ] doesn't exist."
TABLE_CREATED_MSG = "The table [ table_name ] created."
TABLE_DELETED_MSG = "The table [ table_name ] deleted."
TABLE_ALREADY_EXIST_MSG = "The table [ table_name ] already exists."
DB_INFO_INI_NOT_EXIST_MSG = DB_INFO_INI + " does't exist."
NO_TABLE_EXIST_MSG = "No table exists."
DB_CONNECTION_ESTABLISHED_MSG = "DB Connection established."
DB_CONNECTION_RELEASED_MSG = "DB Connection released."
