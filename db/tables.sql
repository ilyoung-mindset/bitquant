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

CREATE TABLE `market_schedule` (
  `id` varchar(35) NOT NULL,
  `market` varchar(35) NOT NULL,
  `api` varchar(256) NOT NULL,
  `reqs` varchar(4000)  DEFAULT NULL,
  `req_tpl` varchar(512) DEFAULT NULL,
  `freq` varchar(8) DEFAULT NULL,
  `action` varchar(256) DEFAULT NULL,
  `last_run_time`   bigint(20)  default 0 comment '上次创建时间',
  `next_run_time`   bigint(20)  default 0 comment '下次创建时间',
  `update_time` varchar(14) DEFAULT NULL,
  `create_date` varchar(8) DEFAULT NULL,
  `create_time` varchar(14) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4  

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
  `last_run_time`  timestamp default '0000-00-00 00:00:00' comment '首次创建时间',
  `update_time` varchar(14) DEFAULT NULL,
  `create_date` varchar(8) DEFAULT NULL,
  `create_time` varchar(14) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4  

  CREATE TABLE base_job
    (
        app_id varchar(128) not null comment '应用 id',
        job_group varchar(128) not null comment '任务组',
        job_id varchar(128) not null comment '任务 id',
        type varchar(32) comment '任务类型',
        expression varchar(4000) comment '任务表达式',
        `data` varchar(4000) comment '任务数据',
        transactional char(1) comment '任务是否需要运行在事务中',
        concurrent char(1) comment '任务是否可以并发执行',
        description varchar(256) comment '描述',
        first_create timestamp default '0000-00-00 00:00:00' comment '首次创建时间',
        last_update timestamp default current_timestamp on update current_timestamp comment '上次更新时间',
        version int comment '数据版本',
        upd_user varchar(20) comment '数据更新用户',
        upd_date char(8) comment '数据更新日期',
        upd_time char(14) comment '数据更新时间',
        apv_user varchar(20) comment '数据审核/拒绝用户',
        apv_date char(8) comment '数据审核/拒绝日期',
        apv_time char(14) comment '数据审核/拒绝时间',
        crt_user varchar(20) comment '数据创建用户',
        crt_date char(8) comment '数据创建日期',
        crt_time char(14) comment '数据创建时间',
        rsv1 varchar(180) comment '保留字段',
        rsv2 varchar(180) comment '保留字段',
        rsv3 varchar(180) comment '保留字段',
        rsv4 varchar(180) comment '保留字段',
        rsv5 varchar(180) comment '保留字段',
        primary key (app_id, job_group, job_id)
    )
    ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='任务控制表';

CREATE TABLE base_job_schedule
    (
        schedule_id varchar(128) not null comment '日程 id',
        app_id varchar(128) comment '应用 id',
        job_group varchar(128) comment '任务组',
        job_id varchar(128) comment '任务 id',
        run_second varchar(32) comment '执行 - 秒',
        run_minute varchar(32) comment '执行 - 分',
        run_hour varchar(32) comment '执行 - 小时',
        run_day_in_month varchar(32) comment '执行 - 日',
        run_month varchar(32) comment '执行 - 月',
        run_day_in_week varchar(32) comment '执行 - 星期几',
        run_year varchar(32) comment '执行 - 年',
        calendar varchar(128) comment '日历',
        status char(1) comment '日程状态',
        description varchar(256) comment '日程描述',
        first_create timestamp default '0000-00-00 00:00:00' comment '首次创建时间',
        last_update timestamp default current_timestamp on update current_timestamp comment '上次更新时间',
        version int comment '数据版本',
        upd_user varchar(20) comment '数据更新用户',
        upd_date char(8) comment '数据更新日期',
        upd_time char(14) comment '数据更新时间',
        apv_user varchar(20) comment '数据审核/拒绝用户',
        apv_date char(8) comment '数据审核/拒绝日期',
        apv_time char(14) comment '数据审核/拒绝时间',
        crt_user varchar(20) comment '数据创建用户',
        crt_date char(8) comment '数据创建日期',
        crt_time char(14) comment '数据创建时间',
        rsv1 varchar(180) comment '保留字段',
        rsv2 varchar(180) comment '保留字段',
        rsv3 varchar(180) comment '保留字段',
        rsv4 varchar(180) comment '保留字段',
        rsv5 varchar(180) comment '保留字段',
        primary key (schedule_id)
    )
    ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='任务日程表';
    
    
    
    
    
    CREATE TABLE base_job_schedule_state
    (
        schedule_id varchar(128) not null comment '日程 id',
        app_id varchar(128) comment '应用 id',
        job_group varchar(128) comment '任务组',
        job_id varchar(128) comment '任务 id',
        run_second varchar(32) comment '执行 - 秒',
        run_minute varchar(32) comment '执行 - 分',
        run_hour varchar(32) comment '执行 - 小时',
        run_day_in_month varchar(32) comment '执行 - 日',
        run_month varchar(32) comment '执行 - 月',
        run_day_in_week varchar(32) comment '执行 - 星期几',
        run_year varchar(32) comment '执行 - 年',
        calendar varchar(128) comment '日历',
        status char(1) comment '日程状态',
        triger_name varchar(128) ,
        triger_params varchar(256) ,
        description varchar(256) comment '日程描述',
        data_version timestamp default '0000-00-00 00:00:00' comment '首次创建时间',
        last_run_time timestamp default '0000-00-00 00:00:00' comment '首次创建时间',
        next_next_time timestamp default '0000-00-00 00:00:00' comment '首次创建时间',
        first_create timestamp default '0000-00-00 00:00:00' comment '首次创建时间',
        last_update timestamp default current_timestamp on update current_timestamp comment '上次更新时间',
        primary key (schedule_id)
    )
    ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='任务日程状态';