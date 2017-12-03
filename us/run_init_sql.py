import sys
sys.path.append("..")

from util import ts
from pysql import db_init
from util import log
import config

log_name	= 'run_init_sql'
abs_log_file ="%s/%s.%s.log" % (config.LOG_DIR,log_name,ts.dir_time())
log.log_init(abs_log_file)
db_init.run(config)
# abs_log_file ="%s/daily_collection.%s.log" % (config.LOG_DIR,ts.dir_time())
# collection.run(config,abs_log_file)


