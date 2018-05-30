create database ueface;

create table people
(
id varchar(36) primary key not null comment '主键',
name VARCHAR(20) not null comment '名称',
image_path varchar(100) not null comment '图片的存储路径',
create_time DATETIME DEFAULT CURRENT_TIMESTAMP comment '创建时间',
description VARCHAR(100)  comment '备注'
) comment='人信息表';

create table cammap
(
id int primary key AUTO_INCREMENT comment '主键',
map_name VARCHAR(20) not null comment '主键',
image varbinary(1024) not null comment '图片的二进制数据', 
create_time DATETIME DEFAULT CURRENT_TIMESTAMP comment '创建时间',
description VARCHAR(100) comment '备注'
) comment='地图表';


create table camera
(
id int primary key AUTO_INCREMENT comment '主键',
cam_name VARCHAR(20) not null  comment '摄像头名称',
map_id int not null comment '外键,地图表id',
url varchar(100) not null comment '该摄像头的对应流媒体地址',
x float not null comment '横坐标',
y float not null  comment '纵坐标',
create_time DATETIME DEFAULT CURRENT_TIMESTAMP  comment '创建时间',
description VARCHAR(100)  comment '备注'
) comment='摄像头表';


create table camframe
(
id varchar(36) primary key comment 'uuid,主键',
cam_id int not null comment '外键,摄像头ID',
framebytes MEDIUMBLOB not null comment '帧的二进制数据',
create_time DATETIME DEFAULT CURRENT_TIMESTAMP  comment '创建时间',
description VARCHAR(100)  comment '备注'
) comment='帧表';

create table recognition
(
id varchar(36) primary key comment 'uuid,主键',
cap_img MEDIUMBLOB not null comment '从帧中扣出的头像',
cam_id int not null comment  '外键,摄像头ID',
frame_id int not null comment '外建,所属帧ID',
user_id int not null comment '外键,该头像识别得到的人id',
cap_time DATETIME not null comment '被捕捉到的时间',
create_time DATETIME DEFAULT CURRENT_TIMESTAMP  comment '创建时间',
description VARCHAR(100)  comment '备注'
) comment='识别结果表';












