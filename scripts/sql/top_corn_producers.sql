WITH 
  temp_table AS
  (SELECT
    state_name,
    commodity_desc,
    SUM(value) AS total_produce,
    TIMESTAMP_TRUNC(load_time, YEAR) AS year_load,
  FROM 
    `bigquery-public-data.usda_nass_agriculture.crops`
  WHERE
    group_desc='FIELD CROPS' AND
    statisticcat_desc='PRODUCTION' AND
    agg_level_desc='STATE' AND
    value IS NOT NULL AND
    unit_desc='BU'
  GROUP BY
    commodity_desc,
    year_load,
    state_name
  ORDER BY
    state_name,
    commodity_desc,
    total_produce DESC)
SELECT
  state_name,
  commodity_desc,
  MAX(total_produce) AS total_prod
FROM
  temp_table
WHERE
  year_load='2018-01-01 00:00:00 UTC' AND
  commodity_desc='CORN'
GROUP BY
  state_name,
  commodity_desc
ORDER BY
  state_name
