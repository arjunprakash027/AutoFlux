{{
    config(
        materialized = "table",
        tags = ["staging"]
    )
}}

With TRAIN_DATA as (
    SELECT *
    ,   1 as use_for_training
    FROM {{source('input_data','train')}}
)

SELECT * FROM TRAIN_DATA