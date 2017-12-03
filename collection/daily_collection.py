#!/usr/bin/python
# -*- coding: UTF-8 -*-


from urllib2 import urlopen,Request
import json
import MySQLdb
import time
import os
import types
import logging

import sys
sys.path.append("..")
from pysql import db_init
from pysql import t_stock_security
from pysql import t_stock_history_day
from util import ts
from util import mail

def getKLine(security_id):
	ret = False
	url = 'https://www.futunn.com/quote/k-line?security_id=%s&type=2' % (security_id)
	response = ''
	try:
		request = Request(url)
		response = urlopen(request,timeout=10).read()
		if len(response) < 15:
			# log.write("%f get data from url=%s fail\n" %(time.time(),url))
			logging.error("%f get data from url=%s fail" %(time.time(),url))
			raise IOError('no data!')
	except Exception as e:
		# print(e,security_id)
		logging.error(e)
		logging.error(security_id)

	if response is '':
		return ret,response

	OK='0'
	d = json.loads(response)
	if d['code'] == OK:
		ret = True
	return ret,d



def getBasic(security_id):
	ret = False
	url = 'https://www.futunn.com/trade/quote-basic?security_id=%s' % (security_id)
	response = ''
	try:
		request = Request(url)
		response = urlopen(request,timeout=10).read()
		if len(response) < 15:
			# log.write("%f get data from url=%s fail\n" %(time.time(),url))
			logging.error("%f get data from url=%s fail" %(time.time(),url))
			raise IOError('no data!')
	except Exception as e:
		# print(e)
		logging.error(e)
		logging.error(security_id)

	if response is '':
		return ret,response

	OK='0'
	d = json.loads(response)
	if d['code'] == OK:
		ret = True

	return ret,d



def run(config):
	logging.info("daily_collection start")
	conn	= db_init.GetDBConn(config)
	stocks	= t_stock_security.QueryTable(conn)

	stocks_num = 0
	stocks_data_num = 0
	for stock in stocks:
		start_tick = time.clock()
		insert_data_num = 0
		#print(stock)
		#if stock['stock_id']!=u'JD':
		#	continue

		stock_id 	= MySQLdb.escape_string(stock['stock_id'])
		stock_name	= MySQLdb.escape_string(stock['stock_name'])
		se			= MySQLdb.escape_string(stock['exchange'])
		ext_info	= ''
		ret,kline = getKLine(stock['security_id'])
		if not ret:
			logging.error("getKline err for stock=%s" %(stock_name))
			continue

		last_data = t_stock_history_day.GetLastInsertData(conn,stock_id)
		max_day_ts = 0
		if len(last_data) != 0:
			max_day_ts=last_data[0]['day_ts']

		has_basic,basic = getBasic(stock['security_id'])

		for i,v in enumerate(kline['data']['list']):

			if v['k'] <= max_day_ts :
				continue

			circulation,market_value,eps = 0,0,0
			if ts.is_today_ts(v['k']) and has_basic:
				market_value = (float)(basic['data']['quote']['mv'])
				eps 	= (float)(basic['data']['quote']['eps'])
				price 	= (float)(basic['data']['quote']['price'])
				if price == 0:
					logging.error("getBasic for stock=%s but price=0" %(stock_name))
					continue
				circulation = (int)(market_value/price)

			stocks_data_num += 1
			insert_data_num += 1
			t_stock_history_day.InsertData(conn,stock_name,stock_id,se,v['k'],
											v['o'],v['c'],v['h'],v['l'],
											v['v'],v['t'],circulation,market_value,eps,ext_info)
			conn.commit()
		end_tick = time.clock()
		elapsed = end_tick - start_tick
		logging.info("collect data for stock=%s cost time=%f,insert data num=%d" %(stock_name,elapsed,insert_data_num))
	conn.close()
	logging.info("daily_collection end")



	

