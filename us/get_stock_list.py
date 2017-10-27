#!/usr/bin/python
# -*- coding: UTF-8 -*-


from urllib2 import urlopen,Request
import json
import MySQLdb
import time
import os
import ts
import types
import config

def getStocks(plate_type,page):
	ret = False
	#://www.futunn.com/stock/top-list?plate_id=200303&sort_direct=2&page=0&_=1497666924665 
	url = 'https://www.futunn.com/stock/top-list?plate_id=%s&sort_direct=%s&page=%d' \
			% (plate_type, config.STOCK_SORT_DIRECT_UP,page)
	response = ''
	try:
		request = Request(url)
		response = urlopen(request,timeout=10).read()
		if len(response) < 15:
			raise IOError('no data!')
	except Exception as e:
		print(e,plate_type,page)
	if response is '':
		return ret,response

	OK='0'
	d = json.loads(response,encoding='utf-8')
	if d['code'] == OK:
		ret = True

	return ret,d
	
# all us stocks
def getUsStocks(page):
	return getStocks(config.STOCK_PLATE_ID_US,page)


# stock index
def getStockIndex(page):
	return getStocks(config.STOCK_PLATE_ID_US_INDEX,page)


def getNyseStocks(page):
	return getStocks(config.STOCK_PLATE_ID_NYSE,page)

def getAmexStocks(page):
	return getStocks(config.STOCK_PLATE_ID_AMEX,page)

def getNasqadStocks(page):
	return getStocks(config.STOCK_PLATE_ID_NASDAQ,page)


def run():
	file="%s/get_stock_list.%s.log" % (config.LOG_DIR,ts.dir_time())
	print(file)
	if not os.path.exists(file):
		os.system('touch %s' % file)
	log=open(file,'a')
	log.write("%s get_stock_list start\n" %(ts.htime(0)))

	conn= MySQLdb.connect(
			host	= config.DB_CONFIG['HOST'],
			port 	= config.DB_CONFIG['PORT'],
			user	= config.DB_CONFIG['USER'],
			passwd	= config.DB_CONFIG['PASS'],
			db 		= config.DB_CONFIG['DB'],
			)
	cur = conn.cursor()


	tbl = config.TABLE_CONFIG['stock2securityId']

	plate_list = []
	plate_list.append(config.STOCK_PLATE_ID_NYSE)
	plate_list.append(config.STOCK_PLATE_ID_AMEX)
	plate_list.append(config.STOCK_PLATE_ID_NASDAQ)
	plate_list.append(config.STOCK_PLATE_ID_US_INDEX)

	for plate in plate_list:
		se = 'us'
		stock_num = 0
		max_stock_num = 1000000
		if plate == config.STOCK_PLATE_ID_NYSE:
			se = 'nyse'
		if plate == config.STOCK_PLATE_ID_AMEX:
			se = 'amex'
		if plate == config.STOCK_PLATE_ID_NASDAQ:
			se = 'nasqad'
		if plate == config.STOCK_PLATE_ID_US_INDEX:
			se = 'usindex'

		for k in range(0,max_stock_num):
			ret,stocks = getStocks(plate,k)

			if not ret:
				log.write("getMLine err for page=%d\n" %(page))
				continue

			if not (stocks.has_key('data')):
				log.write("getMLine err has not data for stock=%s\n" %(stock_name))
				continue

			if not type(stocks['data']) == dict :
				log.write("getMLine err has not list for stock=%s\n" %(stock_name))
				continue

			if len(stocks['data']['list']) == 0:
				log.write("get stock done,stock_num=%s\n" %(stock_num))
				break

			for i,v in enumerate(stocks['data']['list']):
				stock_num = stock_num + 1

				id 		= v['security_id']
				code	= v['security_code']
				name	= v['security_name']

				if type(id) == types.UnicodeType:
					id = id.encode('utf-8')
				if type(code) == types.UnicodeType:
					code = code.encode('utf-8')
				if type(name) == types.UnicodeType:
					name = name.encode('utf-8')

				if type(id) == types.IntType:
					id = str(id)
				if type(code) == types.IntType:
					code = str(code)
				if type(id) == types.IntType:
					name = str(name)

				id		= MySQLdb.escape_string(id)
				code	= MySQLdb.escape_string(code)
				name	= MySQLdb.escape_string(name)

				query = "replace into %s (stock_id,stock_exchange,stock_name,security_id) values('%s','%s','%s','%s')" \
						% (tbl,code,se,name,id)
				cur.execute(query)

			conn.commit()

		log.write("%s get_stock_list se=%s,stock_num=%d\n" %(ts.htime(0),se,stock_num))



	log.write("%s get_stock_list end\n" %(ts.htime(0)))
	log.close()
	cur.close()
	conn.close()



run()
	

