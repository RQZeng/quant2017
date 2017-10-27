import sys
sys.path.append("..")

from util import ts
from strategy import double_ma
import config

abs_log_file ="%s/daily_strategy_dma.%s.log" % (config.LOG_DIR,ts.dir_time())
double_ma.run(config,abs_log_file)


