import sys
sys.path.append("..")

from util import ts
from stock_init import stock_init
from util import log
import config

log_name	= 'run_init_stock'
abs_log_file ="%s/%s.%s.log" % (config.LOG_DIR,log_name,ts.dir_time())
log.log_init(abs_log_file)
stock_init.run(config,config.US_PLATE)
# abs_log_file ="%s/daily_collection.%s.log" % (config.LOG_DIR,ts.dir_time())
# collection.run(config,abs_log_file)


