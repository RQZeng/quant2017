import time
import calendar

def ts():
	return int(round(time.time()))

def mts():
	return int(round(time.time()*1000))

def day_ts():
	lt=time.localtime()
	mkt=time.mktime((lt.tm_year,lt.tm_mon,lt.tm_mday,0,0,0,0,0,0))
	return int(round(mkt))

def is_today_ts(ts):
	lt=time.localtime(ts)
	mkt=time.mktime((lt.tm_year,lt.tm_mon,lt.tm_mday,0,0,0,0,0,0))
	dts = int(round(mkt))
	if dts == day_ts():
		return True
	return False
	

def month_ts():
	lt=time.localtime()
	mkt=time.mktime((lt.tm_year,lt.tm_mon,1,0,0,0,0,0,0))
	return int(round(mkt))

def last_month_ts(curr_month_ts):
	if curr_month_ts == 0:
		curr_month_ts = month_ts()

	lt=time.localtime(curr_month_ts-1)
	days = calendar.monthrange(lt.tm_year,lt.tm_mon)[1]
	DAY_SEC = 24 * 60 * 60
	lmts = curr_month_ts - days * DAY_SEC
	return lmts

def htime(ts_t=None):
	if ts_t is None:
		ts_t = ts()
	if ts_t == 0:
		ts_t = ts()
	return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(ts_t))

def dir_time(ts_t = None):
	if ts_t is None:
		ts_t = ts()
	return time.strftime("%Y-%m-%d-%H%M%S",time.localtime(ts_t))

def test():
	print('ts=%d' %(ts()))
	print('mts=%d' %(mts()))
	print('day_ts=%d' %(day_ts()))
	print('htime=%s' %(htime()))
	print('dir_time=%s' %(dir_time()))
	val_month_ts = []
	for i in range(200):
		curr_month_ts = 0
		if i == 0:
			curr_month_ts = month_ts()
			print('curr_month_ts i=%02d,month_ts=%d,human time=%s' %(i,curr_month_ts,htime(curr_month_ts)))
		else:
			curr_month_ts = val_month_ts[i-1]
	
		val_month_ts.append(last_month_ts(curr_month_ts))
		print('i=%002d,month_ts=%d,human time=%s' %(i,val_month_ts[i],htime(val_month_ts[i])))
	

# end
