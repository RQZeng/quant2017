#!/bin/bash

mysql_host='127.0.0.1'
mysql_port=3306
mysql_user='root'
mysql_pass='root'

# databases name
db_array=(
db_stock_us
)

function create_table(){
    sql_file=$1
	for i in ${db_array[@]}; do
    	mysql -h$mysql_host -u$mysql_user -p$mysql_pass $i <$sql_file
	done
}

for file in `ls ./*.sql`; do
    create_table $file
done


