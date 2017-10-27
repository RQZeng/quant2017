from urllib2 import urlopen,Request
import json
import MySQLdb
import time
import os
import ts
import config

def run():
	file="%s/daily_calc_ma.%s.log" % (config.LOG_DIR,ts.dir_time())
	print(file)
	if not os.path.exists(file):
		os.system('touch %s' % file)
	log=open(file,'a')
	log.write("%s daily_calc_ma start\n" %(ts.htime(0)))

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
	# stocks.append({'id':'00700'})

	day_sec = 24*60*60
	day_ts = ts.day_ts()
	insert_sql_num = 0
	stocks_num = 0
	for stock in stocks:
		stocks_num += 1
		stock_id	= stock['id']

		stock_max_day_ts = 0
		max_day_ts_query = "select max(day_ts) from %s where stock_id='%s'" % \
				(config.TABLE_CONFIG['stockAnalysisMa'],stock_id)
		cur.execute(max_day_ts_query)
		results = cur.fetchall()
		for row in results:
			if row[0] != None:
				stock_max_day_ts = row[0]

		for day_ts_i in range(day_ts,stock_max_day_ts,-day_sec):
			get_day_60_query = "select * from %s \
					where stock_id='%s' and stock_day_ts <= %d \
					order by stock_day_ts desc limit 60" % \
					(config.TABLE_CONFIG['stockDayHistory'],stock_id,day_ts_i)
			cur.execute(get_day_60_query)
			results = cur.fetchall()
			if len(results)<60:
				break
			
			ma_day_ts = results[0][3]
			close	  = results[0][5]
			ma05_data = [row[5] for row in results[0:5]]
			ma10_data = [row[5] for row in results[0:10]]
			ma20_data = [row[5] for row in results[0:20]]
			ma30_data = [row[5] for row in results[0:30]]
			ma60_data = [row[5] for row in results[0:60]]
			ma5  = sum(ma05_data)/len(ma05_data)
			ma10 = sum(ma10_data)/len(ma10_data)
			ma20 = sum(ma20_data)/len(ma20_data)
			ma30 = sum(ma30_data)/len(ma30_data)
			ma60 = sum(ma60_data)/len(ma60_data)
			add_stock_ma_query = "replace into %s (stock_id,day_ts,close,ma5,ma10,ma20,ma30,ma60) \
			values('%s',%d,%d,%.3f,%.3f,%.3f,%.3f,%.3f)" \
					% (config.TABLE_CONFIG['stockAnalysisMa'],stock_id,ma_day_ts,close,ma5,ma10,ma20,ma30,ma60)
			#print(add_stock_ma_query)
			cur.execute(add_stock_ma_query)
			insert_sql_num += 1

		conn.commit()


	log.write("%f search stock_num=%d, insert data=%d\n" %(time.time(),stocks_num,insert_sql_num))
	log.write("%f daily_calc_ma end\n" %(time.time()))
	log.close()
	cur.close()
	conn.close()



run()
	

