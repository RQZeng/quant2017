#!/bin/sh
python /data/quantitativeTrading/sz/daily_collection.py
python /data/quantitativeTrading/sz/daily_collection_min.py
python /data/quantitativeTrading/sz/daily_calc_ma.py
python /data/quantitativeTrading/sz/daily_strategy_dma.py
# python /root/futu/daily_analysis_ma.py
# python /root/futu/daily_month_profit_calc.py
