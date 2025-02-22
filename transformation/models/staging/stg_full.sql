{{
    config(
        materialized = "table",
        tags = ["staging"]
    )
}}

{{ union_by_column(['stg_train','stg_test']) }}

