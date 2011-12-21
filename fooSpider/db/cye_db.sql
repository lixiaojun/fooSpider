drop table if exists cye_tb;
create table cye_tb(
	id int(32) not null auto_increment,
	url varchar(300) not null,
	title varchar(600) not null,
	price varchar(100) not null,
	price_img_url varchar(300) not null,
	product_img_url varchar(300) not null,
	detail text not null,
	primary key(id)
)engine=innodb default charset=utf8;