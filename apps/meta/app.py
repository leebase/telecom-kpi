"""Metadata-driven Streamlit stub that renders subject areas from YAML."""
from __future__ import annotations

import os
import sys
from functools import lru_cache
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:  # pragma: no cover - Streamlit runtime
    sys.path.insert(0, str(SRC))

from data.metadata_provider import MetadataDataProvider
from metadata_runtime import MetadataConfig, MetadataLoadError, load_metadata
from ui.layout_engine import render_subject_area

_DEFAULT_METADATA_PATH = Path(__file__).resolve().parents[2] / "metadata" / "dashboard_telco.yaml"
_METADATA_ENV_VAR = "DASHBOARD_METADATA_PATH"


@lru_cache(maxsize=1)
def _load_pack(path: str) -> MetadataConfig:
    return load_metadata(path, force_reload=False)


def _resolve_metadata_path() -> Path:
    env_path = os.getenv(_METADATA_ENV_VAR)
    if env_path:
        return Path(env_path).expanduser().resolve()

    secret_path = None
    if hasattr(st, "secrets"):
        try:
            secrets_obj = st.secrets
            secret_path = secrets_obj.get("metadata_path") if secrets_obj else None
        except Exception:
            secret_path = None
    if secret_path:
        return Path(secret_path).expanduser().resolve()

    return _DEFAULT_METADATA_PATH


def _render_sidebar(config: MetadataConfig) -> None:
    st.sidebar.title("Metadata Pack")
    st.sidebar.markdown(
        f"**Pack ID:** `{config.pack_id}`\n\n"
        f"**Schema:** {config.schema_version}\n\n"
        f"**App Version:** {config.app_version}"
    )
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Data Sources**")
    for name, source in config.data_sources.items():
        location = source.dsn_env or source.path or "(configured elsewhere)"
        st.sidebar.write(f"- `{name}` → {source.dialect} ({location})")


def _build_resolver(provider: MetadataDataProvider, kpi_map, chart_map):
    def resolver(slot_type: str, slot_value: str):
        if slot_type == "kpi_card" and slot_value in kpi_map:
            kpi = kpi_map[slot_value]
            dataset_id = kpi.widgets.primary.dataset
            payload = provider.build_kpi_payload(kpi, dataset_id)
            return kpi.widgets.primary.type, payload

        if slot_type == "chart" and slot_value in chart_map:
            kpi, chart = chart_map[slot_value]
            unit = kpi.widgets.primary.unit or ""
            title = chart.encoding.get("title") if chart.encoding else kpi.title
            payload = provider.build_chart_payload(chart.dataset, title, unit)
            return chart.type, payload

        message = f"{slot_type.title()} '{slot_value}' coming soon"
        return "placeholder", {"message": message}

    return resolver


def main() -> None:
    st.set_page_config(page_title="Metadata Dashboard", layout="wide")
    st.title("Metadata-Driven Dashboard Stub")

    metadata_path = _resolve_metadata_path()
    try:
        config = _load_pack(str(metadata_path))
    except FileNotFoundError:
        st.error(f"Metadata file not found at {metadata_path}")
        st.stop()
    except MetadataLoadError as exc:
        st.error("Metadata validation failed. See logs for details.")
        with st.expander("Validation errors"):
            for error in exc.errors:
                loc = ".".join(str(part) for part in error.get("loc", [])) or "root"
                st.write(f"`{loc}` → {error.get('msg')}")
        st.stop()

    provider = MetadataDataProvider(config)
    _render_sidebar(config)

    kpi_map = {kpi.id: kpi for kpi in config.kpis}
    chart_map = {}
    for kpi in config.kpis:
        for chart in kpi.widgets.secondary:
            if chart.chart_id:
                chart_map[chart.chart_id] = (kpi, chart)

    tab_labels = [area.title for area in config.subject_areas]
    tabs = st.tabs(tab_labels)

    for tab, area in zip(tabs, config.subject_areas):
        with tab:
            if area.id == "network_performance":
                resolver = _build_resolver(provider, kpi_map, chart_map)
                render_subject_area(area, resolver)
            else:
                st.subheader(area.title)
                st.info("This subject area will be migrated to the metadata runtime in Sprint 3.")

    st.success("Metadata loaded once per session. Refresh the page to re-read the pack.")


if __name__ == "__main__":  # pragma: no cover
    main()
