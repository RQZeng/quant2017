CREATE TABLE IF NOT EXISTS `t_stock_month_profit` (
	`stock_id`			varchar(32) NOT NULL COMMENT '股票id',
	`month_ts`			int(10) unsigned NOT NULL COMMENT '此数据的的月时间戳',
	`last_month_close`	decimal(30,5) NOT NULL COMMENT '上月收盘价',
	`curr_month_close`	decimal(30,5) NOT NULL COMMENT '此月收盘价',
	`diff`				decimal(30,5) NOT NULL COMMENT '变化值',
	`ext_info`			varchar(128) COMMENT '其他信息',
	
	`last_update_ts`      timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '上次更新时间戳',
	PRIMARY KEY (`stock_id`,`month_ts`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

source procedure_check_col_exist.sql;
set @db_name    = database();
set @tbl_name   = 't_stock_month_profit';
set @col_name   = 'none';

-- @TODO
-- define you column you want to add
-- set @col_name                = 'test';
-- set @field_define    = concat('ALTER TABLE `',@tbl_name,'` ADD COLUMN `',@col_name,'` INT(10) UNSIGNED NOT NULL DEFAULT 0 COMMENT \'测试\'');
-- call addColIfNotExist(@col_name,@field_define);

DROP PROCEDURE IF EXISTS `addColIfNotExist`;




