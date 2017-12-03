#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
sys.path.append("..")

import MySQLdb
import logging
from util import ts

def TableName():
	table_name	= "t_stock_security"
	return table_name


def DropTable(conn):
	if conn == None:
		return
	cursor = conn.cursor()
	cursor.execute("DROP TABLE IF EXISTS %s" %(TableName()))
	cursor.close()

def CreateTable(conn):
	if conn == None:
		return
	cursor = conn.cursor()
	create_sql 	= """
	CREATE TABLE IF NOT EXISTS `%s` (
		`stock_id`			varchar(32) NOT NULL COMMENT '股票id',
		`exchange`			varchar(32) NOT NULL COMMENT '股票交易所,(hk,sh,sz,us)',
		`stock_name`		varchar(128) COMMENT '股票名字',
		`security_id`		varchar(128) NOT NULL COMMENT '富途的股票id对应的安全id的映射',
		`ext_info`			varchar(128) COMMENT '其他信息',
		
		`last_update_ts`      timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '上次更新时间戳',
		PRIMARY KEY (`stock_id`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8;
	""" %(TableName())
	logging.error(create_sql)
	cursor.execute(create_sql)
	cursor.close()

def InsertTable(conn,insert_sql):
	if conn  == None:
		return

	#logging.error(insert_sql)
	cursor = conn.cursor()
	cursor.execute(insert_sql)
	cursor.close()

def InsertData(conn,stock_id,exchange,stock_name,security_id,ext_info=""):
	query = "replace into %s (stock_id,exchange,stock_name,security_id,ext_info) values('%s','%s','%s','%s','%s')" \
		% (TableName(),stock_id,exchange,stock_name,security_id,ext_info)
	InsertTable(conn,query)


def QueryTable(conn):
	query_sql = "select * from %s" %(TableName())
	#cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
	cursor = conn.cursor()
	cursor.execute(query_sql)
	results = cursor.fetchall() #type(results) == tuple

	#for row in results:
	#	print(row)
	# 	type(row)==dict
	# 	pass
	cursor.close()
	return results


