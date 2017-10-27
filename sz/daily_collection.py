#!/usr/bin/python
# -*- coding: UTF-8 -*-


from urllib2 import urlopen,Request
import json
import MySQLdb
import time
import os
import types
import ts
import config

def getKLine(security_id):
	ret = False
	url = 'https://www.futunn.com/quote/k-line?security_id=%s&type=2' % (security_id)
	response = ''
	try:
		request = Request(url)
		response = urlopen(request,timeout=10).read()
		if len(response) < 15:
			# log.write("%f get data from url=%s fail\n" %(time.time(),url))
			raise IOError('no data!')
	except Exception as e:
		print(e,security_id)

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
			raise IOError('no data!')
	except Exception as e:
		print(e)

	if response is '':
		return ret,response

	OK='0'
	d = json.loads(response)
	if d['code'] == OK:
		ret = True

	return ret,d



def run():
	file="%s/daily_collection.%s.log" % (config.LOG_DIR,ts.dir_time())
	print(file)
	if not os.path.exists(file):
		os.system('touch %s' % file)
	log=open(file,'a')
	log.write("%s daily_collection start\n" %(ts.htime(0)))

	conn= MySQLdb.connect(
			host	= config.DB_CONFIG['HOST'],
			port 	= config.DB_CONFIG['PORT'],
			user	= config.DB_CONFIG['USER'],
			passwd	= config.DB_CONFIG['PASS'],
			db 		= config.DB_CONFIG['DB'],
			charset	= "utf8",
			)
	cur = conn.cursor()
	cur.execute('select * from %s order by stock_id desc' %(config.TABLE_CONFIG['stock2securityId']))
	results = cur.fetchall()

	# get stock
	stocks = []
	for row in results:
		stock = {'id':row[0],'se':row[1],'name':row[2],'sid':row[3]}
		stocks.append(stock)

	# stocks = []
	# stocks.append({'id':'14144','se':'hk','name':'ac','sid':'73499775350592'})
	# stocks.append({'id':'BLW','se':'nyse','name':'BLW信托','sid':'202931'})
	# stocks.append({'id':'03062','se':'hk','name':'xdb','sid':'63101659515894'})
	# stocks.append({'id':'03063','se':'hk','name':'xdb','sid':'63101659515895'})
	# stocks.append({'id':'00890','se':'hk','name':'REP','sid':'37237366457210'})

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

		# log.write("getKLine for stock=%s,security_id=%s\n" %(stock_name,security_id))
		# log.write("getKLine for security_id=%s\n" %(security_id))
		# print("getKLine for security_id=%s\n" %(security_id))
		stock_name	= MySQLdb.escape_string(stock_name)

		ret,kline = getKLine(security_id)

		if not ret:
			log.write("getKLine err for stock=%s\n" %(stock_name))
			continue


		stock_max_day_ts = 0
		max_day_ts_query = "select max(stock_day_ts) from %s where stock_id='%s' and stock_exchange='%s'" % (config.TABLE_CONFIG['stockDayHistory'],stock_id,se)
		cur.execute(max_day_ts_query)
		results = cur.fetchall()
		for row in results:
			if row[0] != None:
				stock_max_day_ts = row[0]


		for i,v in enumerate(kline['data']['list']):
			if v['k'] <= stock_max_day_ts :
				continue

			circulation,market_value,eps = 0,0,0
			if v['k'] == ts.day_ts():
				ret,basic = getBasic(security_id)
				if not ret:
					log.write("getBasic err for stock=%s\n" %(stock_name))
					continue
				else:
					market_value = (float)(basic['data']['quote']['mv'])
					eps = (float)(basic['data']['quote']['eps'])
					price = (float)(basic['data']['quote']['price'])
					if price == 0:
						log.write("getBasic for stock=%s but price=0\n" %(stock_name))
						continue
					circulation = (int)(market_value/price)

			stocks_data_num += 1
			add_stock_history_query = "replace into %s(stock_name,stock_id,stock_exchange,stock_day_ts,open,close,high,low,volumn,turnover,circulation,market_value,eps,ext_info) \
					values('%s','%s','%s',%d,%d,%d,%d,%d,%d,%d,%d,%.03f,%.03f,'%s')" \
					% (config.TABLE_CONFIG['stockDayHistory'],stock_name,stock_id,se,v['k'],v['o'],v['c'],v['h'],v['l'],v['v'],v['t'],circulation,market_value,eps,source)
			cur.execute(add_stock_history_query)
		conn.commit()

	log.write("%s search stock_num=%d, insert data=%d\n" %(ts.htime(0),stocks_num,stocks_data_num))
	log.write("%s daily_collection end\n" %(ts.htime(0)))
	log.close()
	cur.close()
	conn.close()



run()
	

