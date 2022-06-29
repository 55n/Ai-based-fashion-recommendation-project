create view sipn as
	select 
			si.*,
            p.product_img_url,
			p.product_brand,
			p.product_number as pid, 
			p.product_season,
			p.product_rating,
			p.product_tag_list,
			p.product_price,
			p.product_size,
            p.product_category_1
		from
			(select 
					s.*,
					i.product_name as pname,
					i.product_page_url as purl
				from (
					select 
							street_snap_model_name,
                            street_snap_page_url,
                            street_snap_shooting_date,
							street_snap_style,
							street_snap_tag_list, 
							street_snap_desc, 
							street_snap_img_url, 
							snap_id, 
							weather_cluster, 
							temperature_cluster, 
							style_label
						from 
							street_snap_tbl
						where
							street_snap_style="캐주얼" or
                            street_snap_style="포멀" or
                            street_snap_style="스트릿" or
                            street_snap_style="아메리칸캐주얼") as s
				join item_tbl i on i.snap_id=s.snap_id) as si
		join product_tbl p on si.purl=p.product_page_url;
    
    
drop view sipn;

select * from sipn limit 1;