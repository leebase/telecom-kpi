"""Synthetic metadata-driven data provider used during refactor."""
from __future__ import annotations

import numpy as np
import pandas as pd

from metadata_runtime.models import KpiConfig, MetadataConfig


class MetadataDataProvider:
    """Returns deterministic stub data for metadata metrics."""

    def __init__(self, config: MetadataConfig) -> None:
        self._config = config
        self._rng_cache = {}
        self._frame_cache = {}

    def _seed_rng(self, metric_id: str) -> np.random.Generator:
        seed = abs(hash(metric_id)) % 10_000
        if metric_id not in self._rng_cache:
            self._rng_cache[metric_id] = np.random.default_rng(seed)
        return self._rng_cache[metric_id]

    def get_metric_frame(self, metric_id: str) -> pd.DataFrame:
        if metric_id in self._frame_cache:
            return self._frame_cache[metric_id]

        rng = self._seed_rng(metric_id)
        dates = pd.date_range(end=pd.Timestamp.utcnow().normalize(), periods=14)
        base = rng.uniform(20, 100)
        trend = rng.normal(loc=0.6, scale=0.3, size=len(dates)).cumsum()
        values = base + trend
        df = pd.DataFrame({"date": dates, "value": values})
        self._frame_cache[metric_id] = df
        return df

    def build_kpi_payload(self, kpi: KpiConfig, metric_id: str) -> dict:
        df = self.get_metric_frame(metric_id)
        latest = df.iloc[-1]["value"]
        previous = df.iloc[-2]["value"] if len(df) > 1 else latest
        delta = latest - previous
        return {
            "label": kpi.title,
            "value": round(latest, 2),
            "delta": round(delta, 2),
            "unit": kpi.widgets.primary.unit or "",
            "tooltip": kpi.description or "",
        }

    def build_chart_payload(self, metric_id: str, title: str, unit: str = "") -> dict:
        df = self.get_metric_frame(metric_id)
        payload = {
            "title": title,
            "y_label": unit or "Value",
            "dataframe": df,
        }
        return payload


__all__ = ["MetadataDataProvider"]
