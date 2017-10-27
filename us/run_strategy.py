import sys
sys.path.append("..")

from util import ts
from strategy import strategy
from util import log
import config

log_name	= 'daily_strategy'
abs_log_file ="%s/%s.%s.log" % (config.LOG_DIR,log_name,ts.dir_time())
log.log_init(abs_log_file)
strategy.run(config)


