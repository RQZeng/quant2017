#!/bin/sh
python /data/quantitativeTrading/sh/daily_collection.py
python /data/quantitativeTrading/sh/daily_collection_min.py
python /data/quantitativeTrading/sh/daily_calc_ma.py
python /data/quantitativeTrading/sh/daily_strategy_dma.py
# python /root/futu/daily_month_profit_calc.py
# python /root/futu/daily_strategy_dma.py
