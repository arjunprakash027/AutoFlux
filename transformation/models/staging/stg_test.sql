{{
    config(
        materialized = "table",
        tags = ["staging"]
    )
}}

WITH TEST_DATA as (
    SELECT *
    ,   0 as use_for_training
    ,   0 as TARGET
    FROM {{source('input_data','test')}}
)

SELECT * FROM TEST_DATA