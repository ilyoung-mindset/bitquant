CREATE TABLE `trade` (
  `id` varchar(35) NOT NULL,
  `market` varchar(64) DEFAULT NULL,
  `symbol` varchar(64) DEFAULT NULL,
  `price`  decimal(65,18) DEFAULT NULL,
  `amount`  decimal(65,18)  DEFAULT NULL COMMENT '金额',
  `time` bigint(20) DEFAULT NULL,
  `direction` varchar(8) DEFAULT NULL,
  `trade_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '第三方交易平台上的交易id',
  `create_date` varchar(8) DEFAULT NULL,
  `create_time` varchar(14) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4  

CREATE TABLE `kline` (
  `id` varchar(35) NOT NULL,
  `market` varchar(64) DEFAULT NULL,
  `symbol` varchar(64) DEFAULT NULL,
  `period` varchar(30) DEFAULT NULL,
  `kid` bigint(20) DEFAULT NULL,
  `count` bigint(20) DEFAULT NULL,
  `amount` decimal(65,18) DEFAULT NULL,
  `open` decimal(65,18) DEFAULT NULL COMMENT '开盘价',
  `close` decimal(65,18) DEFAULT NULL,
  `low` decimal(65,18) DEFAULT NULL,
  `high` decimal(65,18) DEFAULT NULL,
  `vol` decimal(65,18) DEFAULT NULL,
  `create_date` varchar(8) DEFAULT NULL,
  `create_time` varchar(14) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4  

CREATE TABLE `depth` (
  `id` varchar(35) NOT NULL,
  `market` varchar(64) DEFAULT NULL,
  `symbol` varchar(64) DEFAULT NULL,
  `time` bigint(20) DEFAULT NULL,
  `action` varchar(20) DEFAULT NULL,
  `price`  decimal(65,18) DEFAULT NULL,
  `count`  decimal(65,18)  DEFAULT NULL COMMENT '金额',
  `create_date` varchar(8) DEFAULT NULL,
  `create_time` varchar(14) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4  


CREATE TABLE `user` (
  `id` varchar(35) NOT NULL,
  `username` varchar(64) DEFAULT NULL,
  `realname` varchar(64) DEFAULT NULL,
  `neckname` varchar(64) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,  
  `id_no` varchar(32) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `mobile` varchar(32) DEFAULT NULL,
  `create_date` varchar(8) DEFAULT NULL,
  `create_time` varchar(14) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4  

CREATE TABLE `market_user` (
  `uid` varchar(35) NOT NULL,
  `username` varchar(35) NOT NULL,
  `market` varchar(64) DEFAULT NULL,
  `api_id` varchar(255) DEFAULT NULL,
  `api_key` varchar(255) DEFAULT NULL,
  `access_key` varchar(255) DEFAULT NULL,
  `expire_time` bigint(20) DEFAULT NULL,
  `create_date` varchar(8) DEFAULT NULL,
  `create_time` varchar(14) DEFAULT NULL,
  PRIMARY KEY (`uid`,`username`, `market`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4  
 
CREATE TABLE `account` (
  `id` varchar(35) NOT NULL,
  `uid` varchar(35) NOT NULL,
  `market` varchar(64) DEFAULT NULL,
  `act_type` varchar(32) NOT NULL,
  `symbol` varchar(64) DEFAULT NULL,
  `bal_amt`  decimal(65,18) DEFAULT NULL  COMMENT '余额',
  `lock_amt`  decimal(65,18)  DEFAULT NULL,
  `create_date` varchar(8) DEFAULT NULL,
  `create_time` varchar(14) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4  

CREATE TABLE `tx` (
  `id` varchar(35) NOT NULL,
  `uid` varchar(35) NOT NULL,
  `strategy_id` varchar(35) NOT NULL,
  `market` varchar(64) DEFAULT NULL,
  `symbol` varchar(64) DEFAULT NULL,
  `time` bigint(20) DEFAULT NULL,
  `action` varchar(20) DEFAULT NULL,
  `status` varchar(8) DEFAULT NULL,
  `price`  decimal(65,18) DEFAULT NULL,
  `count`  decimal(65,18)  DEFAULT NULL COMMENT '金额',
  `trade_id` varchar(64)  DEFAULT NULL,
  `end_date` varchar(8) DEFAULT NULL,
  `end_time` varchar(14) DEFAULT NULL,
  `create_date` varchar(8) DEFAULT NULL,
  `create_time` varchar(14) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4  

CREATE TABLE `strategy` (
  `id` varchar(35) NOT NULL,
  `uid` varchar(35) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `amount` decimal(65,18) DEFAULT NULL,
  `freq` char(1) DEFAULT NULL,
  `start_date` char(8) DEFAULT NULL,
  `remarks` varchar(255) DEFAULT NULL,
  `time_limit` varchar(14) DEFAULT NULL,
  `create_date` varchar(8) DEFAULT NULL,
  `create_time` varchar(14) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4  

CREATE TABLE `strategy_log` (
  `id` varchar(35) NOT NULL,
  `strategy_id` varchar(35) NOT NULL,
  `uid` varchar(35) NOT NULL,
  `end_time` varchar(14) DEFAULT NULL,
  `create_date` varchar(8) DEFAULT NULL,
  `create_time` varchar(14) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4  


CREATE TABLE `strategy_schedule` (
  `id` varchar(35) NOT NULL,
  `strategy_id` varchar(35) NOT NULL,
  `uid` varchar(35) NOT NULL,
  `freq` char(1) DEFAULT NULL,
  `time` varchar(14) DEFAULT NULL,
  `action` varchar(14) DEFAULT NULL,
  `create_date` varchar(8) DEFAULT NULL,
  `create_time` varchar(14) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4  




