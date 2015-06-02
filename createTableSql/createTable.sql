CREATE TABLE `stock_holder_info` (
	`code` varchar(100) DEFAULT NULL COMMENT '股票代码',
	`holder_name` varchar(100) DEFAULT NULL COMMENT '流通股东名称',
	`position_num` decimal(20,4) DEFAULT NULL COMMENT '持股数量',
	`position_rate` decimal(5,4) DEFAULT NULL COMMENT '持股比例'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;