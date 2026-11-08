{# Uses the exact schema name. By default dbt would create `public_gold`. #}
{% macro generate_schema_name(custom_schema_name, node) %}
    {% if custom_schema_name is not none %}
        {{ custom_schema_name | trim }}
    {% else %}
        {{ target.schema | trim }}
    {% endif %}
{% endmacro %}
