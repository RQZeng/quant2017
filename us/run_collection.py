#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
sys.path.append("..")

reload(sys)                        
sys.setdefaultencoding('utf-8')   

from util import ts
from collection import collection
from util import log
import config

log_name	= 'daily_collection'
abs_log_file ="%s/%s.%s.log" % (config.LOG_DIR,log_name,ts.dir_time())
log.log_init(abs_log_file)
collection.run(config)
# abs_log_file ="%s/daily_collection.%s.log" % (config.LOG_DIR,ts.dir_time())
# collection.run(config,abs_log_file)


