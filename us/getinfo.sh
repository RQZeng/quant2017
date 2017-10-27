#!/bin/sh

#data
#se='hk' #Stock Exchange
#code='00700'
#code='00434'
#code='99993'
basic_json='basic.json'
kline_day='kline_day.json'

#clear
rm -rf $basic_json
rm -rf $kline_day


stock2scurityid(){
	se=$1
	code=$2
	#tmp file
	cookies='cookies.txt'
	index_tmp_file='index.html'
	stock_tmp_file='stock.html'
	log_file="${se}_result.txt"
	wget --save-cookies $cookies  -O $index_tmp_file --keep-session-cookies https://www.futunn.com 2>/dev/null
	wget --load-cookies $cookies -O $stock_tmp_file "https://www.futunn.com/quote/stock?m=$se&code=$code" 2>/dev/null
	
	security_id=`grep 'securityId' $stock_tmp_file|awk -F "[=;']" '{print $3}'` 
	stock_name=`grep -rF 'keywords' $stock_tmp_file|awk -F '[" -]' '{print $15}'`
	if [ -n "$security_id" ]; then
		echo "find security_id=$security_id for $stock_name $se$code" >> $log_file
		mysql -u${DB_USER} -p${DB_PASS} ${DB_NAME} -e "replace into ${DB_TBL}(stock_id,stock_exchange,stock_name,security_id) values('${code}','${se}','${stock_name}','${security_id}')"
	else
		echo "find no security_id for $se$code" >> $log_file 
	fi
	# wget -O $basic_json https://www.futunn.com/trade/quote-basic?security_id=$security_id 2>/dev/null
	# wget -O $kline_day https://www.futunn.com/quote/k-line?security_id=$security_id&type=2 2>/dev/null
	
	rm -rf $index_tmp_file
	rm -rf $stock_tmp_file
	rm -rf $cookies 
}


######################
# config exchange
# stock_exchange='hk'
# stock_id_min=0
# stock_id_max=99999
# stock_exchange='sh'
# stock_id_min=0
# stock_id_max=999999
#stock_exchange='sz'
#stock_id_min=0
#stock_id_max=999999
#######################

stock_exchange='us'
DB_USER='root'
DB_PASS='root'
DB_NAME='db_stock_us'
DB_TBL="t_stock_security"
for line in `cat us_result.txt`; do
	#echo $line
	stock=${line##*,}
	stock2scurityid $stock_exchange $stock
	#sleep 0.1
done

