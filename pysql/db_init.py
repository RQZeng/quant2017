#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
sys.path.append("..")

import MySQLdb
import MySQLdb.cursors
from util import ts
import t_stock_security
import t_stock_history_day

def run(config):
	CreateDataBase(config)
	CreateTable(config)

def GetConn(config):
	host	= config.DB_CONFIG['HOST']
	user	= config.DB_CONFIG['USER']
	pw		= config.DB_CONFIG['PASS']
	db_name	= config.DB_CONFIG['DB']
	# return data with list
	#conn 	= MySQLdb.connect(host, user, pw, charset='utf8')
	#
	# return data with dict
	conn 	= MySQLdb.connect(host, user, pw, charset='utf8',cursorclass=MySQLdb.cursors.DictCursor)
	return conn


def CreateDataBase(config):
	conn	= GetConn(config)

	cursor 	= conn.cursor()
	db_name	= config.DB_CONFIG['DB']
	cursor.execute("""create database if not exists %s""" %(db_name))
	cursor.close()

def GetDBConn(config):
	conn	= GetConn(config)
	db_name	= config.DB_CONFIG['DB']
	conn.select_db(db_name)
	return conn

def CreateTable(config):
	conn = GetDBConn(config)
	t_stock_security.CreateTable(conn)
	t_stock_history_day.CreateTable(conn)

	
	
