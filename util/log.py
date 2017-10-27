#/usr/local/env python

import logging


def log_init(logfile=None):
	if logfile == None:
		logfile = '/data/quantitativeTrading/util/redbird.log'
	
	# level : noset < debug < info < warning < error < critical
	logging.basicConfig(level=logging.DEBUG,
			format='%(levelname)s %(asctime)s %(filename)s[line:%(lineno)d] %(message)s',
			datefmt='%a, %d %b %Y %H:%M:%S',
			filename=logfile,
			filemode='w')



if __name__ == "__main__":
    #log.info(msg[, *args[, **kwargs]])
    #log.warning(msg[, *args[, **kwargs]])
    #log.error(msg[, *args[, **kwargs]])
    #log.critical(msg[, *args[, **kwargs]])
	log_init('test')
    # log.setLevel(logging.INFO)
	log = logging.getLogger('test')

    # log.debug("test %s", "hello")
    # log.info("test %s", "hello")
    # log.warning("test %s", "hello")
    # log.error("test %s", "hello")
    # log.critical("test %s", "hello")
    # log.critical("test %s %s" %('test1','test2'))
