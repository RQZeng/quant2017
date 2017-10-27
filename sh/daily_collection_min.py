#!/usr/bin/python
# -*- coding: UTF-8 -*-

from urllib2 import urlopen,Request
import json
import MySQLdb
import time
import os
import ts
import config

def getMLine(security_id):
	ret = False
	url = 'https://www.futunn.com/trade/quote-minute?security_id=%s' %(security_id)
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
	file="%s/daily_collection_min.%s.log" % (config.LOG_DIR,ts.dir_time())
	if not os.path.exists(file):
		os.system('touch %s' % file)
	log=open(file,'a')
	log.write("%f daily_collection_min start\n" %(time.time()))

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
		ret,mline = getMLine(security_id)
		log.write("getMLine for stock=%s\n" %(stock_name))

		if not ret:
			log.write("getMLine err for stock=%s\n" %(stock_name))
			continue


		if not (mline.has_key('data')):
			log.write("getMLine err has not data for stock=%s\n" %(stock_name))
			continue

		if not type(mline['data']) == dict :
			log.write("getMLine err has not list for stock=%s\n" %(stock_name))
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

	log.write("%f search stock_num=%d, insert data=%d\n" %(time.time(),stocks_num,stocks_data_num))
	log.write("%f daily_collection end\n" %(time.time()))
	log.close()
	cur.close()
	conn.close()



run()
	

