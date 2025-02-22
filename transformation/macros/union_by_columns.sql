{% macro union_by_column(table_names) %}
    {% if not table_names or table_names | length == 0 %}
        {{ exeptions.raise_compiler_error("Tables does not exist") }}
    {% endif %}

    {% set all_cols = [] %}
    {% set table_columns = {} %}

    {% for table_name in table_names %}
        {% set relation = ref(table_name) %}
        
        {% if not relation %}
            {{ expections.raise_compiler_error("Table " + table_name + " does not exist") }}
        {% endif %}

        {% set cols = adapter.get_columns_in_relation(relation) %}
        {% set cols = cols | map(attribute="name") | list %}

        {% do table_columns.update({table_name:cols}) %}

        {% for col in cols %}
            {% if col not in all_cols %}
                {% do all_cols.append(col) %}
            {% endif %}
        {% endfor %}
    {% endfor %}

    {% for table_name in table_names %}
        {% set relation = ref(table_name) %}
        {% set select_cols = [] %}
        {% set cols = table_columns[table_name] %}

        {% for col in all_cols %}
            {% if col in cols %}
                {% do select_cols.append(col) %}
            {% else %}
                {% do select_cols.append("NULL AS" ~ col) %}
            {% endif %}
        {% endfor %}

        {% if loop.first %}
            SELECT {{ select_cols | join(",")}} FROM {{ relation}}
        {% else %}
            UNION ALL
            SELECT {{ select_cols | join(",")}} FROM {{ relation}}
        {% endif %}
    {% endfor %}

{% endmacro %}