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
from util import ts
from util import mail

def getMLine(security_id):
	ret = False
	url = 'https://www.futunn.com/trade/quote-minute?security_id=%s' %(security_id)
	response = ''
	try:
		request = Request(url)
		response = urlopen(request,timeout=10).read()
		if len(response) < 15:
			# log.write("%f get data from url=%s fail\n" %(time.time(),url))
			logging.error("get data from url=%s fail" %(url))
			raise IOError('no data!')
	except Exception as e:
		# print(e)
		logging.error(e)

	if response is '':
		return ret,response

	OK='0'
	d = json.loads(response)
	if d['code'] == OK:
		ret = True

	return ret,d



def run(config):
	logging.error("daily_collection_min start")

	conn= MySQLdb.connect(
			host	= config.DB_CONFIG['HOST'],
			port 	= config.DB_CONFIG['PORT'],
			user	= config.DB_CONFIG['USER'],
			passwd	= config.DB_CONFIG['PASS'],
			db 		= config.DB_CONFIG['DB'],
			)
	cur = conn.cursor()
	cur.execute('select * from %s' %(config.TABLE_CONFIG['stock2securityId']))
	results = cur.fetchall()

	# get stock
	stocks = []
	for row in results:
		stock = {'id':row[0],'se':row[1],'name':row[2],'sid':row[3]}
		stocks.append(stock)

	# stocks = []
	# stocks.append({'id':'00700','se':'hk','name':"qq",'sid':'54047868453564'})
	# stocks.append({'id':'01833','se':'hk','name':"yintai",'sid':'58372900521769'})
	stocks = []
	stocks.append({'id':'AAPL','se':'nasqad','name':'AAPL','sid':'205189'})

	stocks_num = 0
	stocks_data_num = 0
	source = 'futu'
	for stock in stocks:
		stocks_num += 1
		# time.sleep(0.01)
		response 	= ''
		stock_name 	= stock['name']
		stock_id	= stock['id']
		se			= stock['se']
		security_id = stock['sid']

		if type(stock_name) == types.UnicodeType:
			stock_name = stock_name.encode('utf-8')
		if type(stock_id) == types.UnicodeType:
			stock_id = stock_id.encode('utf-8')
		if type(se) == types.UnicodeType:
			se= se.encode('utf-8')
		if type(security_id) == types.UnicodeType:
			security_id= security_id.encode('utf-8')
		stock_name	= MySQLdb.escape_string(stock_name)

		# log.write("getKLine for stock=%s,security_id=%s\n" %(stock_name,security_id))
		# log.write("getKLine for security_id=%s\n" %(security_id))
		ret,mline = getMLine(security_id)
		# log.write("getMLine for stock=%s\n" %(stock_name))

		if not ret:
			# log.write("getMLine err for stock=%s\n" %(stock_name))
			logging.error("getMLine err for stock=%s" %(stock_name))
			continue


		if not (mline.has_key('data')):
			# log.write("getMLine err has not data for stock=%s\n" %(stock_name))
			logging.error("getMLine err has not data for stock=%s" %(stock_name))
			continue

		if not type(mline['data']) == dict :
			# log.write("getMLine err has not list for stock=%s\n" %(stock_name))
			logging.info("getMLine err has not list for stock=%s" %(stock_name))
			continue


		#print('stock=%s' %(stock_id))


		for i,v in enumerate(mline['data']['list']):
			#print(v)
			stocks_data_num += 1
			add_stock_history_query = "replace into t_stock_history_min(stock_name,stock_id,stock_exchange,data_ts,price,volume,turnover,ratio,ext_info) \
					values('%s','%s','%s',%d,%d,%d,%d,%.03f,'%s')" \
					% (stock_name,stock_id,se,v['time'],v['price'],v['volume'],v['turnover'],v['ratio'],source)
			#print(add_stock_history_query)
			cur.execute(add_stock_history_query)
		conn.commit()

	logging.info("%f search stock_num=%d, insert data=%d" %(time.time(),stocks_num,stocks_data_num))
	logging.info("%f daily_collection end" %(time.time()))
	# log.write("%f search stock_num=%d, insert data=%d\n" %(time.time(),stocks_num,stocks_data_num))
	# log.write("%f daily_collection end\n" %(time.time()))
	# log.close()
	cur.close()
	conn.close()




