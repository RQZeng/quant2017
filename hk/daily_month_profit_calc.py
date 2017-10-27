from urllib2 import urlopen,Request
import json
import MySQLdb
import time
import os
import ts

def run():
	file="/root/futu/log/daily_month_profit_calc.%d.log" % (ts.ts())
	if not os.path.exists(file):
		os.system('touch %s' % file)
	log=open(file,'a')
	log.write("%f daily_calc_ma start\n" %(time.time()))

	conn= MySQLdb.connect(
			host='localhost',
			port = 3306,
			user='root',
			passwd='root',
			db ='db_stock',
			)
	cur = conn.cursor()
	cur.execute('select * from t_stock_futu')
	results = cur.fetchall()

	# get stock
	stocks = []
	for row in results:
		stock = {'id':row[0],'se':row[1],'name':row[2],'sid':row[3]}
		stocks.append(stock)
	
	# stocks = []
	# stocks.append({'id':'00700'})

	curr_mts = ts.month_ts()
	insert_sql_num = 0
	stocks_num = 0
	for stock in stocks:
		stocks_num += 1
		stock_id	= stock['id']

		stock_max_ts = 0 
		max_ts_query = "select max(month_ts) from t_stock_month_profit_hk where stock_id='%s'" % (stock_id)
		cur.execute(max_ts_query)
		results = cur.fetchall()
		for row in results:
			if row[0] != None:
				stock_max_ts = row[0]

		target_mts = ts.last_month_ts(curr_mts) # calc from last month
		while target_mts > stock_max_ts:
			last_mts = ts.last_month_ts(target_mts)
			get_month_data_query = "select * from t_stock_history where stock_id='%s' and stock_day_ts < %d and stock_day_ts >= %d order by stock_day_ts desc" \
								%(stock_id,target_mts,last_mts)
			# print(get_month_data_query)
			cur.execute(get_month_data_query)
			results = cur.fetchall()
			if len(results)<=0:
				print('break at ts=%s for stock=%s' %(ts.htime(last_mts),stock_id))
				break
			# print('get stock[%s] data %d at ts=%s' %(stock_id,len(results),ts.htime(last_mts)))

			min_idx = 0
			max_idx = len(results)-1
			end_month_close = results[min_idx][5]
			start_month_close = results[max_idx][5]
			
			#print('%s close=%.3f' %(ts.htime(results[min_idx][3]),results[min_idx][5]))
			#print('%s close=%.3f' %(ts.htime(results[max_idx][3]),results[max_idx][5]))
			add_stock_profit_query = "replace into t_stock_month_profit_hk(stock_id,month_ts,last_month_close,curr_month_close,diff) \
						values('%s',%d,%.3f,%.3f,%.3f)" \
					% (stock_id,last_mts,start_month_close,end_month_close,(end_month_close-start_month_close))
			cur.execute(add_stock_profit_query)
			target_mts = last_mts
			insert_sql_num += 1

		conn.commit()


	log.write("%f search stock_num=%d, insert data=%d\n" %(time.time(),stocks_num,insert_sql_num))
	log.write("%f daily_calc_ma end\n" %(time.time()))
	log.close()
	cur.close()
	conn.close()



run()
	

