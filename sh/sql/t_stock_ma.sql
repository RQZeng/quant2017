CREATE TABLE IF NOT EXISTS `t_stock_ma` (
	`stock_id`			varchar(32) NOT NULL COMMENT '股票id',
	`day_ts`			int(10) unsigned NOT NULL COMMENT '此数据的的天时间戳',
	`close`				decimal(30,5) NOT NULL COMMENT '收盘价',
	`ma5`				decimal(30,5) NOT NULL COMMENT 'ma5',
	`ma10`				decimal(30,5) NOT NULL COMMENT 'ma10',
	`ma20`				decimal(30,5) NOT NULL COMMENT 'ma20',
	`ma30`				decimal(30,5) NOT NULL COMMENT 'ma30',
	`ma60`				decimal(30,5) NOT NULL COMMENT 'ma60',
	`ext_info`			varchar(128) COMMENT '其他信息',
	
	`last_update_ts`      timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '上次更新时间戳',
	PRIMARY KEY (`stock_id`,`day_ts`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

source procedure_check_col_exist.sql;
set @db_name    = database();
set @tbl_name   = 't_stock_ma';
set @col_name   = 'none';

-- @TODO
-- define you column you want to add
-- set @col_name                = 'test';
-- set @field_define    = concat('ALTER TABLE `',@tbl_name,'` ADD COLUMN `',@col_name,'` INT(10) UNSIGNED NOT NULL DEFAULT 0 COMMENT \'测试\'');
-- call addColIfNotExist(@col_name,@field_define);

DROP PROCEDURE IF EXISTS `addColIfNotExist`;




