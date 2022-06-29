-- 인덱스 생성하는 쿼리임


alter table street_snap_tbl drop index snap_idx;
create index snap_idx
on street_snap_tbl(rownum asc, style_label);


alter table item_tbl drop index item_idx;
create index item_idx
on item_tbl(rownum asc, snap_id, product_page_url);



-- 유사한 상품을 무엇으로 찾아올 지 아직 결정하지 못했기 때문에 고민할 여지가 있음
alter table product_tbl drop index product_idx;
create index product_idx
on product_tbl(rownum asc, product_category_1, product_number);



alter table daily_forecast_tbl drop index daily_forecast_idx;
create index daily_forecast_idx
on daily_forecast_tbl (weather_cluster, temperature_cluster);

alter table similar_product_tbl drop index similar_product_idx;
create index similar_product_idx
on similar_product_tbl(rownum asc, product_number);
