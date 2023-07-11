-- Top Mushroom Producers (LB) per State in 2022

WITH
  temp_table AS
  (SELECT
    state_name,
    commodity_desc,
    SUM(value) as total_produce,
    TIMESTAMP_TRUNC(load_time, YEAR) AS year_load,
  FROM 
    `bigquery-public-data.usda_nass_agriculture.crops`
  WHERE
    group_desc='HORTICULTURE' AND
    statisticcat_desc='PRODUCTION' AND
    agg_level_desc='STATE' AND
    commodity_desc='MUSHROOMS' AND
    value IS NOT NULL
  GROUP BY
    state_name,
    commodity_desc,
    year_load)
SELECT
  state_name,
  commodity_desc,
  MAX(total_produce) AS total_prod
FROM
  temp_table
WHERE
  year_load='2022-01-01 00:00:00 UTC'
GROUP BY
  state_name,
  commodity_desc
ORDER BY
  total_prod DESC
  
