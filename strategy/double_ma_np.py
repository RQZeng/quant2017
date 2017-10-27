#!/usr/bin/env python  
# -*- coding: UTF-8 -*-  


import json
import MySQLdb
import time
import os
import math
import logging

import sys
sys.path.append("..")
from util import ts
from util import mail

	
def run(config):
	logging.info("%s double ma start" %(ts.htime()))

	conn= MySQLdb.connect(
			host	= config.DB_CONFIG['HOST'],
			port 	= config.DB_CONFIG['PORT'],
			user	= config.DB_CONFIG['USER'],
			passwd	= config.DB_CONFIG['PASS'],
			db 		= config.DB_CONFIG['DB'],
			charset	= "utf8",
			)
	cur = conn.cursor()
	cur.execute('select * from %s order by stock_id desc' \
				%(config.TABLE_CONFIG['stock2securityId']))
	results = cur.fetchall()

	# get stock
	stocks = []
	for row in results:
		stock = {'id':row[0],'se':row[1],'name':row[2],'sid':row[3]}
		stocks.append(stock)
	
	stocks = []
	stocks.append({'id':'AAPL'})

	day_ts = ts.day_ts()
	for stock in stocks:
		stock_id	= stock['id']
		se			= stock['se']
		limit 		= 70

		query		= "select * from %s \
						where stock_id='%s' and stock_day_ts <= %d \
						order by stock_day_ts desc limit %d" % \
						(config.TABLE_CONFIG['stockDayHistory'],stock_id,day_ts,limit)
		logging.info(query)
	

	logging.info("%f search stock_num=%d, insert data=%d" %(time.time(),stocks_num,insert_sql_num))
	logging.info("%f daily_strategy_dma end" %(time.time()))
	cur.close()
	conn.close()




