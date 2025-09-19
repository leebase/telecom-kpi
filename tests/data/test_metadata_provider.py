from __future__ import annotations

import pandas as pd

from metadata_runtime.models import MetadataConfig
from data.metadata_provider import MetadataDataProvider


def _minimal_metadata() -> MetadataConfig:
    payload = {
        "schema_version": "1.0",
        "app_version": "0.9.0",
        "pack_id": "test",
        "label": "Test",
        "globals": {"timezone": "UTC", "default_date_range": "last_30_days"},
        "dialects": {"default": "snowflake", "supported": ["snowflake"]},
        "data_sources": {
            "snowflake_main": {"dialect": "snowflake", "dsn_env": "SNOWFLAKE_DSN"}
        },
        "filters": {"global": [], "subject_area": {}},
        "subject_areas": [
            {
                "id": "network",
                "title": "Network",
                "layout": {
                    "grid_columns": 12,
                    "sections": [
                        {
                            "id": "cards",
                            "rows": [[{"kpi_card": "kpi_test"}]],
                        }
                    ],
                },
            }
        ],
        "kpis": [
            {
                "id": "kpi_test",
                "title": "Test KPI",
                "subject_area": "network",
                "metrics": [
                    {
                        "id": "metric_test",
                        "data_source": "snowflake_main",
                        "sql": "SELECT 1",
                    }
                ],
                "widgets": {
                    "primary": {
                        "type": "kpi_card",
                        "dataset": "metric_test",
                        "unit": "",
                    },
                    "secondary": [],
                },
            }
        ],
        "auxiliary_metrics": [],
    }
    return MetadataConfig.parse_obj(payload)


def test_metric_frame_generation():
    config = _minimal_metadata()
    provider = MetadataDataProvider(config)
    df = provider.get_metric_frame("metric_test")
    assert isinstance(df, pd.DataFrame)
    assert {"date", "value"}.issubset(df.columns)


def test_build_kpi_payload():
    config = _minimal_metadata()
    provider = MetadataDataProvider(config)
    payload = provider.build_kpi_payload(config.kpis[0], "metric_test")
    assert payload["label"] == "Test KPI"
    assert "value" in payload and "delta" in payload
