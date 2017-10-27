#!/usr/bin/env python  
# -*- coding: UTF-8 -*-  


import json
import MySQLdb
import time
import os
import math
import logging

import pandas as pd 

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
	
	# stocks = []
	# stocks.append({'id':'AAPL','se':'nasqad'})

	day_ts = ts.day_ts()
	htime	= ts.htime()
	mail_subjuect = 'Double MA for %s' %(htime)
	mail_text = ''
	mail_stock_num = 0

	for stock in stocks:
		stock_id	= stock['id']
		se			= stock['se']
		limit 		= 70

		query		= "select * from %s \
						where stock_id='%s' and stock_day_ts <= %d \
						order by stock_day_ts desc limit %d" % \
						(config.TABLE_CONFIG['stockDayHistory'],stock_id,day_ts,limit)

		df = pd.read_sql(query,con=conn)

		if len(df) == 0:
			logging.info('none data for %s' %(stock_id))
			continue
		date_index = []
		for v in df['stock_day_ts']:
			d =  time.localtime(v)
			d = time.strftime("%Y-%m-%d %H:%M:%S",d)
			date_index.append(d)
		dates = pd.to_datetime(date_index)

		df.index = dates
		df.sort_values('stock_day_ts', inplace=True)

		ma_day_list = [5,10,20,60]
		ma_list = {}
		for ma_day in ma_day_list:
			ma_day_str = str(ma_day)
			ma = df['close'].rolling(ma_day).mean()
			ma_list['ma_'+ma_day_str] = ma
			ema = df['close'].ewm(span=ma_day).mean()
			ma_list['ema_'+ma_day_str] = ma

		for (k,v) in ma_list.items():
			pass

		SD	= 0.05
		short_mean = ma_list['ma_10'][-1]
		last_short_mean = ma_list['ma_10'][-2]
		long_mean = ma_list['ma_60'][-1]
		flag = True if (short_mean-long_mean)>SD*long_mean else False
		if flag:
			if last_short_mean > short_mean:
				mail_stock_num = mail_stock_num + 1
				mail_text = mail_text + "%s.%s,time=%s buyin\n" %(stock_id,se,htime)
				logging.info('%s buyin' %(stock_id))
		else:
			# mail_text = mail_text + "%s.%s,time=%s sellout\n" %(stock_id,se,htime)
			logging.info('%s sellout' %(stock_id))


		if mail_stock_num > 1000:
			mail.SendMail(mail_subjuect,mail_text)
			mail_stock_num = 0
			mail_text = ''


	mail.SendMail(mail_subjuect,mail_text)
	logging.info("daily_strategy_dma end")
	cur.close()
	conn.close()




