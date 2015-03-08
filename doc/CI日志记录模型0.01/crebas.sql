/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2014/9/2 14:00:33                            */
/*==============================================================*/


drop table if exists ci_log.tmp_data_compare;

rename table ci_log.data_compare to tmp_data_compare;

drop table if exists ci_log.tmp_data_transfer;

rename table ci_log.data_transfer to tmp_data_transfer;

drop table if exists ci_log.run_record;

drop table if exists ci_log.tmp_tips;

rename table ci_log.tips to tmp_tips;

drop table if exists ci_log.tmp_data_dict;

/*==============================================================*/
/* Table: data_compare                                          */
/*==============================================================*/
create table data_compare
(
   session_id           int,
   cmp_id               int,
   cmp_type             smallint,
   cmp_is_success       smallint,
   cmp_fsn              int
);

insert into data_compare (cmp_id, cmp_type, cmp_is_success, cmp_fsn)
select cmp_id, cmp_type, cmp_is_success, cmp_fsn
from ci_log.tmp_data_compare;

/*==============================================================*/
/* Table: data_dict                                             */
/*==============================================================*/
create table data_dict
(
   tb_name              varchar(32) not null,
   fd_name              varchar(32) not null,
   fd_value             smallint not null,
   fd_mean              varchar(32),
   enum_name            char(100),
   type                 smallint,
   seq                  smallint,
   remark               varchar(32),
   primary key (tb_name, fd_name, fd_value)
);

/*==============================================================*/
/* Table: data_transfer                                         */
/*==============================================================*/
create table data_transfer
(
   tran_id              int not null,
   session_id           int,
   tran_tv_sec          int,
   tran_tv_usec         int,
   tran_cycle           int,
   tran_type            smallint,
   tran_is_success      smallint,
   tran_try_count       smallint,
   primary key (tran_id)
);

insert into data_transfer (tran_id, tran_tv_sec, tran_tv_usec, tran_cycle, tran_type, tran_is_success, tran_try_count)
select tran_id, tran_tv_sec, tran_tv_usec, tran_cycle, tran_type, tran_is_success, tran_try_count
from ci_log.tmp_data_transfer;

/*==============================================================*/
/* Table: session                                               */
/*==============================================================*/
create table session
(
   session_id           int not null,
   run_counter          int,
   start_tv_sec         int,
   start_tv_usec        int,
   end_tv_sec           int,
   end_tv_usec          int,
   local_tv_sec         int,
   local_tv_usec        int,
   ip                   char(16),
   series_state         smallint,
   cpu_state            smallint,
   primary key (session_id)
);

/*==============================================================*/
/* Table: tips                                                  */
/*==============================================================*/
create table tips
(
   tips_id              int not null,
   session_id           int,
   itps_tv_sec          int,
   tips_tv_usec         int,
   tips_fsn             int,
   tips_type            smallint,
   primary key (tips_id)
);

insert into tips (tips_id, itps_tv_sec, tips_tv_usec, tips_fsn, tips_type)
select tips_id, itps_tv_sec, tips_tv_usec, tips_fsn, tips_type
from ci_log.tmp_tips;

alter table data_compare add constraint FK_CmpRunRecord foreign key (session_id)
      references session (session_id) on delete restrict on update restrict;

alter table data_transfer add constraint FK_TranRunRecord foreign key (session_id)
      references session (session_id) on delete restrict on update restrict;

alter table tips add constraint FK_TipsRunRecord foreign key (session_id)
      references session (session_id) on delete restrict on update restrict;

