from airflow.plugins_manager import AirflowPlugin


class DbtDocsPlugin(AirflowPlugin):
    """Open the dbt docs inside the Airflow UI.

    Cosmos serves the docs but registers its menu item as an external link. `url_route` is
    what makes Airflow render a view in an iframe.
    """

    name = "dbt_docs"
    external_views = [
        {
            "name": "dbt Docs",
            "category": "browse",
            "href": "/cosmos/data_warehouse/dbt_docs_index.html",
            "url_route": "dbt-docs",
        }
    ]
