import json
import MySQLdb
import time
import os
import ts
import math
import mail

def normalization(ma5,ma10,ma20):
	if ma5 == 0 or ma10 == 0 or ma20 == 0:
		return False
	if ma5 == ma10 and ma10 == ma20:
		return False

	ma_max 	= max(ma5,ma10,ma20)
	ma_mean	= (ma5+ma10+ma20)/3
	ma_min	= min(ma5,ma10,ma20)
	ma_normal = math.sqrt( (math.pow(ma5,2) + math.pow(ma10,2) + math.pow(ma20,2) )/3)

	yma5 	= (ma5-	ma_min)/(ma_max-ma_min)
	yma10 	= (ma10-ma_min)/(ma_max-ma_min)
	yma20 	= (ma20-ma_min)/(ma_max-ma_min)
	#yma5 	= (ma5-	ma_mean)/(ma_max-ma_min)
	#yma10 	= (ma10-ma_mean)/(ma_max-ma_min)
	#yma20 	= (ma20-ma_mean)/(ma_max-ma_min)

	#yma5	= math.log(ma5)
	#yma10	= math.log(ma10)
	#yma20	= math.log(ma20)

	# yma5	= math.pow(0.5,ma5)
	# yma10	= math.pow(0.5,ma10)
	# yma20	= math.pow(0.5,ma20)

	yma5	= (ma5 - ma_mean)/ma_normal
	yma10	= (ma10 - ma_mean)/ma_normal
	yma20	= (ma20 - ma_mean)/ma_normal

	yma5	= (ma5  ) /ma_max 
	yma10	= (ma10 )/ma_max
	yma20	= (ma20 )/ma_max


	na		= (yma5 + yma10 + yma20)/3
	n5		= (yma5 -na)**2 
	n10		= (yma10-na)**2
	n20		= (yma20-na)**2

	normal 	= math.sqrt((n5 + n10 + n20)/3)

	#print(ma5,ma10,ma20)
	#print(ma_max,ma_min)
	# print(yma5,yma10,yma20)

	#if ma_max - ma_min <=3 :
	if normal <= 0.001:
		#print(ma5,ma10,ma20,yma5,yma10,yma20,normal)
		return True

	return False

	
def run():
	file="/root/futu/log/daily_analysis_ma.%d.log" % (ts.ts())
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

	day_sec = 24*60*60
	day_ts = ts.day_ts()
	insert_sql_num = 0
	stocks_num = 0
	
	mail_subjuect = 'MA analysisi for %s' %(time.strftime('%Y-%m-%d',time.localtime(day_ts)))
	mail_text = ''
	for stock in stocks:
		stocks_num += 1
		stock_id	= stock['id']

		stock_max_day_ts = 0
		max_day_ts_query = "select max(day_ts) from t_stock_ma_hk where stock_id='%s'" % (stock_id)
		cur.execute(max_day_ts_query)
		results = cur.fetchall()
		for row in results:
			if row[0] != None:
				stock_max_day_ts = row[0]


		get_day_60_query = "select * from t_stock_ma_hk where stock_id='%s' order by day_ts desc limit 60" % (stock_id)
		cur.execute(get_day_60_query)
		results = cur.fetchall()
		if len(results)<60:
			break

		for row in results:
			day_ts,close = row[1],float(row[2])
			htime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(day_ts))
			# print('data for %s day ts=%s' %(stock_id,htime))
			ma5,ma10,ma20,ma30,ma60 = float(row[3]),float(row[4]),float(row[5]),float(row[6]),float(row[7])
			if normalization(ma5,ma10,ma20) and close > ma5 and day_ts == stock_max_day_ts:
				mail_text = mail_text + "HK%s,time=%s\n" %(stock_id,htime)
				print(stock_id,htime,close,ma5,ma10,ma20,ma30,ma60)
		
		insert_sql_num += 1


	mail.SendMail(mail_subjuect,mail_text)
	log.write("%f search stock_num=%d, insert data=%d\n" %(time.time(),stocks_num,insert_sql_num))
	log.write("%f daily_calc_ma end\n" %(time.time()))
	log.close()
	cur.close()
	conn.close()



run()
	

