#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
sys.path.append("..")

import db_init
import t_stock_security
from us import config

conn = db_init.GetDBConn(config)
t_stock_security.QueryTable(conn)
