#!/usr/bin/python
# -*- coding: UTF-8 -*-

DB_CONFIG = {
	'HOST'	: '127.0.0.1',
	'PORT'	: 3306,
	'USER'	: 'root',
	'PASS'	: 'root',
	'DB'	: 'db_stock_us',
}

TABLE_CONFIG = {
	# table to save collect data 
	'stock2securityId' 	: 't_stock_security',
	'stockDayHistory'	: 't_stock_history_day',
	'stockMinHistory'	: 't_stock_history_min',

	#table to save analysis
	'stockAnalysisMa'			: 't_stock_ma',
	'stockAnalysisMonthProfit'	: 't_stock_month_profit',
}

LOG_DIR = "/data/quantitativeTrading/us/log"


#US
STOCK_PLATE_ID_NYSE 	= '200301' #纽约证券交易所
STOCK_PLATE_ID_NASDAQ 	= '200302' #纳斯达克
STOCK_PLATE_ID_AMEX 	= '200303' #美交所
STOCK_PLATE_ID_US_CN	= '200304' #美股中的中概股
STOCK_PLATE_ID_US_STAR	= '200305' #美股中的明星股
STOCK_PLATE_ID_US 		= '200306' #所有美股
STOCK_PLATE_ID_US_INDEX = '200201' #环球指数

#CN
STOCK_PLATE_ID_SH		= '3000000' #上海主板
STOCK_PLATE_ID_SZ		= '3000001' #深圳主板
STOCK_PLATE_ID_CN_IDX	= '3000002' #沪深指数
STOCK_PLATE_ID_CN_ZXQY	= '3000003' #中小企業
STOCK_PLATE_ID_CN_CYB	= '3000004' #創業板
STOCK_PLATE_ID_CN_A		= '3000005' #沪深A股

#HK
STOCK_PLATE_ID_HK		= '999910' #香港主板
STOCK_PLATE_ID_HK_CYB	= '999911' #香港主板
STOCK_PLATE_ID_HK_IDX	= '999912' #香港主板

STOCK_SORT_DIRECT_DOWN	= '1'
STOCK_SORT_DIRECT_UP 	= '2'

# end
