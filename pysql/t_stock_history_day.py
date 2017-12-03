#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
sys.path.append("..")

import MySQLdb
import logging
from util import ts

def TableName():
	table_name	= "t_stock_history_day"
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
	create_sql 	= """
	CREATE TABLE IF NOT EXISTS `%s` (
		`stock_name`	varchar(128) COMMENT '股票名称',
		`stock_id`		varchar(32) NOT NULL COMMENT '股票id',
		`exchange`		varchar(32) NOT NULL COMMENT '股票交易所,(hk,sh,sz)',
		`day_ts`		int(10) unsigned NOT NULL COMMENT '此数据的的天时间戳',
		`open`			int(10) unsigned NOT NULL COMMENT '今天开盘价(分)',
		`close`			int(10) unsigned NOT NULL COMMENT '昨天收盘价(分)',
		`high`			int(10) unsigned NOT NULL COMMENT '今天最高价(分)',
		`low`			int(10) unsigned NOT NULL COMMENT '今天最低价(分)',
		`volumn`		bigint(20) unsigned NOT NULL COMMENT '成交量(分)',
		`turnover`		bigint(20) unsigned NOT NULL COMMENT '成交额(股)',
		`circulation`	bigint(20) unsigned NOT NULL COMMENT '市场流通(股)',
		`mv`			double NOT NULL COMMENT 'market value,市值',
		`eps`			double NOT NULL COMMENT '市盈率',
		`ext_info`		blob COMMENT '其他信息',
		
		`last_update_ts`      timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '上次更新时间戳',
		PRIMARY KEY (`stock_id`,`day_ts`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8;
	""" %(TableName())
	cursor = conn.cursor()
	cursor.execute(create_sql)
	cursor.close()

def InsertTable(conn,insert_sql):
	if conn  == None:
		return

	cursor = conn.cursor()
	cursor.execute(insert_sql)
	cursor.close()


def InsertData(conn,
	stock_name,stock_id,exchange,day_ts,
	o,c,h,l,
	volumn,turnover,circulation,mv,eps,ext_info=''):
	if conn  == None:
		return
	cursor = conn.cursor()

	query_sql = """
		replace into %s(stock_name,stock_id,exchange,day_ts,
					open,close,high,low,
					volumn,turnover,circulation,mv,eps,ext_info)
				values('%s','%s','%s',%d,
					%d,%d,%d,%d,
					%d,%d,%d,%.03f,%.03f,'%s')
	""" %(TableName(),stock_name,stock_id,exchange,day_ts,
		o,c,h,l,
		volumn,turnover,circulation,mv,eps,ext_info)

	cursor.execute(query_sql)
	cursor.close()


def GetLastInsertData(conn,stock_id):
	cursor = conn.cursor()
	query_sql = "select * from %s where stock_id='%s' order by day_ts desc limit 1" \
				%(TableName(),stock_id) 
	cursor.execute(query_sql)
	results = cursor.fetchall()
	cursor.close()
	return results


