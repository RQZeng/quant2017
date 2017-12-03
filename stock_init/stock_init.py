#!/usr/bin/python                                                                                     
# -*- coding: UTF-8 -*-
 
import sys
import logging
from urllib2 import urlopen,Request
import json
import types
import MySQLdb

sys.path.append("..")
from util import ts
from pysql import db_init
from pysql import t_stock_security
 
def getStocks(plate_type,page,config):
	ret = False
	#://www.futunn.com/stock/top-list?plate_id=200303&sort_direct=2&page=0&_=1497666924665 
	url = 'https://www.futunn.com/stock/top-list?plate_id=%s&sort_direct=%s&page=%d' \
			% (plate_type,config.STOCK_SORT_DIRECT_UP,page)
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
 

 
def run(config,plates):

	for (se,plate) in plates.items():
		stock_num = 0
		max_stock_num = 1000000
		for k in range(0,max_stock_num):
			ret,stocks = getStocks(plate,k,config)

			if not ret:
				logging.error("getMLine err for page=%d\n" %(k))
				continue
			
			if not (stocks.has_key('data')):
				logging.error("getMLine err has not data for stock=%s\n" %(stock_name))
				continue

			if not type(stocks['data']) == dict:
				logging.error("getMLine err has not list for stock=%s\n" %(stock_name))
				continue

			if len(stocks['data']['list']) == 0:
				logging.error("get stock done,stock_num=%s\n" %(stock_num))
				break

			conn = db_init.GetDBConn(config)
			for i,v in enumerate(stocks['data']['list']):
				stock_num = stock_num + 1

				sid     = v['security_id']
				code    = v['security_code']
				name    = v['security_name']
				
				if type(sid) == types.UnicodeType:
				    sid = sid.encode('utf-8')
				if type(code) == types.UnicodeType:
				    code = code.encode('utf-8')
				if type(name) == types.UnicodeType:
				    name = name.encode('utf-8')
				
				if type(sid) == types.IntType:
					sid = str(sid)
				if type(code) == types.IntType:
					code = str(code)
				if type(sid) == types.IntType:
					name = str(name)
					
				sid     = MySQLdb.escape_string(sid)
				code    = MySQLdb.escape_string(code)
				name    = MySQLdb.escape_string(name)
				t_stock_security.InsertData(conn,code,se,name,sid)
			conn.commit()
   
