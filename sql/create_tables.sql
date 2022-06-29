-- 테이블 만드는 쿼리임


use tbtest;


drop table if exists street_snap_tbl;
create table street_snap_tbl(
	street_snap_index int not null,
	street_snap_model_name varchar(20) not null,
    street_snap_page_url varchar(100) not null,
    street_snap_shooting_date varchar(20) not null,
    street_snap_style varchar(20) not null,
    street_snap_tag_list text not null,
    street_snap_desc text not null,
    street_snap_img_url varchar(200) not null,
    snap_id varchar(50) not null primary key,
    weather_cluster tinyint not null,
    temperature_cluster tinyint not null,
    style_label varchar(50) not null
) default character set utf8;

select count(*) from street_snap_tbl;








drop table if exists item_tbl;
create table item_tbl(
    item_index int not null,
	item_name varchar(150) not null,
    snap_id varchar(50) not null,
    item_img_url varchar(150) not null,
    item_tag_list text not null,
    product_name varchar(90) not null,
    product_page_url varchar(150) not null,
    primary key(snap_id, product_page_url)
) default character set utf8;

alter table item_tbl drop constraint fk_item_from_pk_snap;
alter table item_tbl drop constraint fk_item_from_pk_product;

alter table item_tbl
add constraint pk_item
primary key (snap_id, product_page_url);

alter table item_tbl drop foreign key fk_item_from_pk_snap;
alter table item_tbl drop foreign key fk_item_from_pk_product;

alter table item_tbl
add constraint fk_item_from_pk_snap 
foreign key (snap_id)
references street_snap_tbl (snap_id)
ON UPDATE CASCADE ON DELETE RESTRICT;

alter table item_tbl
add constraint fk_item_from_pk_product 
foreign key (product_page_url)
references product_tbl (product_page_url)
ON UPDATE CASCADE ON DELETE RESTRICT;

select count(*) from item_tbl;




drop table if exists product_tbl;
create table product_tbl(
    product_index int not null,
    product_page_url varchar(150) not null primary key,
    product_name varchar(100) not null,
    product_img_url varchar(150) not null,
    product_brand varchar(100) not null,
    product_number varchar(100) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL unique,
    product_season varchar(10) not null,
    product_rating decimal(2,1) not null,
    product_tag_list text not null,
    product_price float not null,
    product_size text not null,
    product_category_1 varchar(20) not null,
    product_category_2 varchar(20) not null,
    product_category_3 varchar(20) not null
) default character set utf8;

select count(*) from product_tbl;





drop table if exists daily_forecast_tbl;
create table daily_forecast_tbl(
	rownum int primary key auto_increment,
    base_date varchar(15) not null unique,
    forecast_date varchar(15) not null unique,
	avg_temp decimal(3,1) not null,
    min_temp decimal(3,1) not null,
    max_temp decimal(3,1) not null,
    pty_time tinyint not null,
    pcp_day decimal(4,1) not null,
    max_wsd decimal(3,1) not null,
    avg_wsd decimal(3,1) not null,
    avg_dew decimal(3,1) not null,
    min_reh decimal(3,1) not null,
    avg_reh decimal(3,1) not null,
    snow decimal(3,1) not null,
    sky_07 tinyint not null,
    sky_13 tinyint not null,
    sky_18 tinyint not null,
    sky_21 tinyint not null,
    pty_07 tinyint not null,
    pty_13 tinyint not null,
    pty_18 tinyint not null,
    pty_21 tinyint not null,
    weather_cluster tinyint not null,
    temperature_cluster tinyint not null
);

select count(*) from daily_forecast_tbl;





drop table if exists similar_product_tbl;
create table similar_product_tbl(
	similar_index int not null,
	product_number varchar(100) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
    similar_product varchar(100) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
    primary key(product_number, similar_product)
) default character set utf8;
select count(*) from similar_product_tbl;

alter table similar_product_tbl drop foreign key fk_product_similar_1;
alter table similar_product_tbl
add constraint fk_product_similar_1
foreign key (product_number)
references product_tbl (product_number)
on update restrict on delete restrict;
