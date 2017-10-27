from urllib2 import urlopen,Request
import json
import MySQLdb
import time
import os
import ts
import math

def normalize(l):
	if len(l) == 0:
		return 0

	avg = sum(l)/len(l)
	t = [(i-avg)**2 for i in (l)]
	n = math.sqrt(sum(t)/len(t))

	return n

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
	
	#stocks = []
	#stocks.append({'id':'00700'})
	#stocks.append({'id':'00434'})

	curr_mts = ts.month_ts()
	insert_sql_num = 0
	stocks_num = 0
	stock_normal_investment = []
	for stock in stocks:
		stocks_num += 1
		stock_id	= stock['id']
		
		profix_query = "select * from t_stock_month_profit_hk where stock_id='%s' order by month_ts desc limit 6" %(stock_id)
		#print(profix_query)
		cur.execute(profix_query)
		results = cur.fetchall()
		month_profix = []

		for row in results:
			mts = row[1]
			lm_close = row[2]
			cm_close = row[3]
			if cm_close == 0 or lm_close == 0:
				#print('stock=%s profix err' %(stock_id))
				month_profix = []
				break
			month_investments = (cm_close-lm_close)/lm_close
			month_profix.append(float(month_investments))

		if len(month_profix)>=6:
			buy_out_price = results[0][3]
			buy_in_price = results[5][3]
			if buy_out_price < buy_in_price:
				continue

			inverst_nor = normalize(month_profix)
			#nor_info = {'id':stock_id,'nor':inverst_nor}
			#stock_normal_investment.append(nor_info)
			nor_info = (stock_id,inverst_nor)
			if inverst_nor == 0:
				print('stock=%s nor err' %(stock_id))
				print(inverst_nor)
				continue

			stock_normal_investment.append(nor_info)


	stock_normal_investment = sorted(stock_normal_investment, key=lambda d : d[1])

	i = 0	
	for v in stock_normal_investment:
		#print('id=%s,nor=%.05f' %(v['id'],v['nor']))
		print('id=%s,nor=%.08f' %(v[0],v[1]))
		i+=1
		if i >10:
			break
		

		

	log.write("%f search stock_num=%d, insert data=%d\n" %(time.time(),stocks_num,insert_sql_num))
	log.write("%f daily_calc_ma end\n" %(time.time()))
	log.close()
	cur.close()
	conn.close()



run()
	

