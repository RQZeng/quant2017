CREATE TABLE IF NOT EXISTS `t_stock_security` (
	`stock_id`			varchar(32) NOT NULL COMMENT '股票id',
	`stock_exchange`	varchar(32) NOT NULL COMMENT '股票交易所,(hk,sh,sz)',
	`stock_name`		varchar(128) COMMENT '股票名字',
	`security_id`		varchar(128) NOT NULL COMMENT '富途的股票id对应的安全id的映射',
	`ext_info`			varchar(128) COMMENT '其他信息',
	
	`last_update_ts`      timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '上次更新时间戳',
	PRIMARY KEY (`stock_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

source procedure_check_col_exist.sql;
set @db_name    = database();
set @tbl_name   = 't_stock_security';
set @col_name   = 'none';

-- @TODO
-- define you column you want to add
-- set @col_name                = 'test';
-- set @field_define    = concat('ALTER TABLE `',@tbl_name,'` ADD COLUMN `',@col_name,'` INT(10) UNSIGNED NOT NULL DEFAULT 0 COMMENT \'测试\'');
-- call addColIfNotExist(@col_name,@field_define);

DROP PROCEDURE IF EXISTS `addColIfNotExist`;




