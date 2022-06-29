-- 프로시저 쿼리임
-- for mysql version 5.7

drop procedure if exists select_worldcup;
delimiter $$
create procedure select_worldcup
(
    in _temp tinyint,
	in _num tinyint
)
begin

	select
		sorted.snap_id,
        sorted.style_label,
        sorted.street_snap_img_url
        from 
			(select 
					snap_id,
					style_label,
                    street_snap_img_url,
					if(@pre<>style_label,@rn:=0,@rn) as label_check,
					@pre:=style_label as label_tmp,
					@rn:=@rn+1 as rownum
				from
					(select 
							*
						from 
							street_snap_tbl
						where 
							find_in_set(style_label, @styles:='0,1,2')
						order by
							rand()) as s,
					 (select @rn:=0) as rn,
					 (select @pre:='') as pre
				where 
					temperature_cluster=_temp
				order by
					style_label asc) as sorted
		where sorted.rownum <= _num;
   
end$$
delimiter ;

call select_worldcup(14, 10);


-- ========================================================================================









drop procedure if exists get_results;
delimiter $$
create procedure get_results
(
	in _weather tinyint,
    in _style varchar(20)
)
begin

select 
pid,
opimg,
opp,
p.product_name,
product_img_url,
product_price,
street_snap_img_url,
product_category_1
from

(select
	*
    from

(select 
street_snap_img_url,
pid,
product_img_url as opimg,
product_price as opp
	from sipn 
	join (select snap_id from street_snap_tbl	
    where weather_cluster=_weather and style_label=_style
	order by rand() limit 1) as snap
	on snap.snap_id=sipn.snap_id) as a

join similar_product_tbl n
on a.pid=n.product_number) as b

join product_tbl p
on p.product_number=b.similar_product;

end$$
delimiter ;

call get_results(87, "0");



-- ============================================================================================================




drop procedure if exists get_else;
delimiter $$
create procedure get_else
(
	in _temp tinyint,
    in _style varchar(20),
    in _cat varchar(20)
)
begin
	select 
		product_name,
		product_img_url,
		product_price,
		product_category_1
		from

		(select
			*
			from

		(select 
		pid
			from sipn 	
			where temperature_cluster=_temp and style_label=_style and product_category_1=_cat order by rand() limit 1) as a

		join similar_product_tbl n
		on a.pid=n.product_number) as b

		join product_tbl p
		on p.product_number=b.similar_product;

end$$
delimiter ;

call get_else(14,"0","아우터");






drop procedure if exists get_results2;
delimiter $$
create procedure get_results2
(
	in _temp tinyint,
    in _style varchar(20)
)
begin

select 
p.product_name,
product_img_url,
product_price,
street_snap_img_url,
product_category_1
from

(select
	*
    from

(select 
street_snap_img_url,
pid
	from sipn 
	join (select snap_id from street_snap_tbl	
    where temperature_cluster=_temp and style_label=_style
	order by rand() limit 1) as snap
	on snap.snap_id=sipn.snap_id) as a

join similar_product_tbl n
on a.pid=n.product_number) as b

join product_tbl p
on p.product_number=b.similar_product;

end$$
delimiter ;


call get_results2(14, "0");
