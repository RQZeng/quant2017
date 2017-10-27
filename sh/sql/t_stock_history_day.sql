CREATE TABLE IF NOT EXISTS `t_stock_history_day` (
	`stock_name`		varchar(128) COMMENT '股票名称',
	`stock_id`			varchar(32) NOT NULL COMMENT '股票id',
	`stock_exchange`	varchar(32) NOT NULL COMMENT '股票交易所,(hk,sh,sz)',
	`stock_day_ts`		int(10) unsigned NOT NULL COMMENT '此数据的的天时间戳',
	`open`				int(10) unsigned NOT NULL COMMENT '今天开盘价(分)',
	`close`				int(10) unsigned NOT NULL COMMENT '昨天收盘价(分)',
	`high`				int(10) unsigned NOT NULL COMMENT '今天最高价(分)',
	`low`				int(10) unsigned NOT NULL COMMENT '今天最低价(分)',
	`volumn`			bigint(20) unsigned NOT NULL COMMENT '成交量(分)',
	`turnover`			bigint(20) unsigned NOT NULL COMMENT '成交额(股)',
	`circulation`		bigint(20) unsigned NOT NULL COMMENT '市场流通(股)',
	`market_value`		double NOT NULL COMMENT '市值',
	`eps`				double NOT NULL COMMENT '市盈率',
	`ext_info`			blob COMMENT '其他信息',
	
	`last_update_ts`      timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '上次更新时间戳',
	PRIMARY KEY (`stock_id`,`stock_day_ts`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

source procedure_check_col_exist.sql;
set @db_name    = database();
set @tbl_name   = 't_stock_history_day';
set @col_name   = 'none';

-- @TODO
-- define you column you want to add
-- set @col_name                = 'test';
-- set @field_define    = concat('ALTER TABLE `',@tbl_name,'` ADD COLUMN `',@col_name,'` INT(10) UNSIGNED NOT NULL DEFAULT 0 COMMENT \'测试\'');
-- call addColIfNotExist(@col_name,@field_define);

DROP PROCEDURE IF EXISTS `addColIfNotExist`;




