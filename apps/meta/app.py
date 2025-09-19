"""Metadata-driven Streamlit stub that renders subject areas from YAML."""
from __future__ import annotations

import os
import sys
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:  # pragma: no cover - Streamlit runtime
    sys.path.insert(0, str(SRC))

from metadata_runtime import MetadataConfig, MetadataLoadError, load_metadata

_DEFAULT_METADATA_PATH = Path(__file__).resolve().parents[2] / "metadata" / "dashboard_telco.yaml"
_METADATA_ENV_VAR = "DASHBOARD_METADATA_PATH"


@lru_cache(maxsize=1)
def _load_pack(path: str) -> MetadataConfig:
    return load_metadata(path, force_reload=False)


def _resolve_metadata_path() -> Path:
    env_path = os.getenv(_METADATA_ENV_VAR)
    if env_path:
        return Path(env_path).expanduser().resolve()

    secret_path = st.secrets.get("metadata_path") if hasattr(st, "secrets") else None
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


def _render_subject_area(area, kpis):
    st.subheader(area.title)
    if area.description:
        st.write(area.description)

    st.markdown("**KPIs**")
    for kpi in kpis:
        st.write(f"- **{kpi.title}** — {kpi.description or 'Description pending.'}")

    st.caption(
        f"Default filters: {', '.join(area.default_filters) if area.default_filters else 'none'}"
    )


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

    _render_sidebar(config)

    kpis_by_area = defaultdict(list)
    for kpi in config.kpis:
        kpis_by_area[kpi.subject_area].append(kpi)

    tab_labels = [area.title for area in config.subject_areas]
    tabs = st.tabs(tab_labels)

    for tab, area in zip(tabs, config.subject_areas):
        with tab:
            _render_subject_area(area, kpis_by_area.get(area.id, []))
            st.info("Widget registry integration coming in the next sprint.")

    st.success("Metadata loaded once per session. Refresh the page to re-read the pack.")


if __name__ == "__main__":  # pragma: no cover
    main()
