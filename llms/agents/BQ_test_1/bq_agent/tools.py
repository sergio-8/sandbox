"""BigQuery helper tools for the NL2SQL agent."""

import logging
import os
from typing import Any

from google.cloud import bigquery

logger = logging.getLogger(__name__)


def list_tables_and_schema(
    project_id: str | None = None,
    dataset_id: str | None = None,
) -> str:
    """List all tables in the configured BigQuery dataset and return their schemas.

    This tool helps the agent understand what data is available before
    generating SQL queries.  Call it at the start of a session or whenever
    the user asks about new tables.

    Args:
        project_id: GCP project ID.  Defaults to the GOOGLE_CLOUD_PROJECT env var.
        dataset_id: BigQuery dataset ID.  Defaults to the BQ_DATASET_ID env var.

    Returns:
        A formatted string describing every table and its columns.
    """
    project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT", "")
    dataset_id = dataset_id or os.environ.get("BQ_DATASET_ID", "")
    bq_location = os.environ.get("BQ_LOCATION", "US")

    if not project_id or not dataset_id:
        return (
            "ERROR: GOOGLE_CLOUD_PROJECT and BQ_DATASET_ID must be set "
            "in the environment before I can list tables."
        )

    client = bigquery.Client(project=project_id, location=bq_location)
    dataset_ref = bigquery.DatasetReference(project_id, dataset_id)

    try:
        tables = list(client.list_tables(dataset_ref))
    except Exception as exc:  # pylint: disable=broad-except
        logger.error("Failed to list tables: %s", exc)
        return f"ERROR listing tables in {project_id}.{dataset_id}: {exc}"

    if not tables:
        return f"No tables found in dataset `{project_id}.{dataset_id}`."

    output_lines: list[str] = [
        f"Dataset: `{project_id}.{dataset_id}`",
        f"Tables ({len(tables)}):",
    ]

    for table_item in tables:
        try:
            table = client.get_table(table_item.reference)
        except Exception as exc:  # pylint: disable=broad-except
            output_lines.append(f"\n### {table_item.table_id}  (schema unavailable: {exc})")
            continue

        output_lines.append(f"\n### `{project_id}.{dataset_id}.{table.table_id}`")
        if table.description:
            output_lines.append(f"Description: {table.description}")
        output_lines.append(f"Rows (approx): {table.num_rows:,}")
        output_lines.append("Columns:")
        for field in table.schema:
            nullable = "NULLABLE" if field.mode == "NULLABLE" else field.mode
            desc = f"  — {field.description}" if field.description else ""
            output_lines.append(f"  - `{field.name}` {field.field_type} ({nullable}){desc}")

    return "\n".join(output_lines)


def get_bigquery_config() -> dict[str, Any]:
    """Return the current BigQuery configuration from environment variables."""
    return {
        "project_id": os.environ.get("GOOGLE_CLOUD_PROJECT", ""),
        "dataset_id": os.environ.get("BQ_DATASET_ID", ""),
        "location": os.environ.get("BQ_LOCATION", "US"),
    }
