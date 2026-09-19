"""
Fiscal Equity Index helpers for UHC budgeting prototypes.

Used by Codes/Project11.ipynb and documented in the repository README.
"""

from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd

DEFAULT_NEED_WEIGHTS = {
    "poverty_rate": 0.3,
    "hiv_prevalence": 0.4,
    "maternal_mortality_ratio": 0.3,
}

# UNICEF SDMX indicator codes (see datasets/metadata/current/_unicefdata_indicators.yaml)
UNICEF_EQUITY_INDICATORS = {
    "poverty_rate": "PV_POP_TOT_PV",
    "maternal_mortality_ratio": "MNCH_MMR",
    "hiv_prevalence": "HVA_EPI_INF_RT",
    "allocated_budget_per_capita": "ECON_GVT_HLTH_EXP_PTGDP",
    "population": "DM_POP_TOT",
}


def compute_health_need_index(
    df: pd.DataFrame,
    *,
    poverty_col: str = "poverty_rate",
    hiv_col: str = "hiv_prevalence",
    mmr_col: str = "maternal_mortality_ratio",
    mmr_scale: float = 1000.0,
    weights: dict[str, float] | None = None,
) -> pd.Series:
    """Weighted need index from poverty, HIV, and maternal mortality."""
    w = weights or DEFAULT_NEED_WEIGHTS
    poverty = df[poverty_col]
    if poverty.max() > 1.5:
        poverty = poverty / 100.0
    hiv = df[hiv_col]
    if hiv.max() > 1.5:
        hiv = hiv / 1000.0
    mmr = df[mmr_col] / mmr_scale
    need = poverty * w["poverty_rate"] + hiv * w["hiv_prevalence"] + mmr * w[
        "maternal_mortality_ratio"
    ]
    if need.max() > 0:
        need = need / need.max()
    return need


def compute_fiscal_equity_index(
    df: pd.DataFrame,
    *,
    entity_col: str = "entity",
    population_col: str = "population",
    allocated_col: str = "allocated_budget_per_capita",
    need_col: str = "health_need_index",
) -> pd.DataFrame:
    """
    Compare observed health spending proxy to need-proportional fair share.

    Returns a copy with expected_budget_per_capita, fiscal_equity_gap, equity_score (0–100).
    """
    out = df.copy()
    if need_col not in out.columns:
        out[need_col] = compute_health_need_index(out)

    total_budget = (out[population_col] * out[allocated_col]).sum()
    fair_per_capita = total_budget / out[population_col].sum()
    out["expected_budget_per_capita"] = fair_per_capita * out[need_col]
    out["fiscal_equity_gap"] = out[allocated_col] - out["expected_budget_per_capita"]

    max_gap = out["fiscal_equity_gap"].abs().max()
    if max_gap == 0 or pd.isna(max_gap):
        out["equity_score"] = 100.0
    else:
        out["equity_score"] = 100 * (1 - (out["fiscal_equity_gap"].abs() / max_gap))

    if entity_col in out.columns:
        out = out.sort_values("equity_score", ascending=False)
    return out


def _latest_country_values(raw: pd.DataFrame, value_col: str = "value") -> pd.DataFrame:
    if raw.empty:
        return raw
    work = raw.copy()
    work["period"] = pd.to_numeric(work["period"], errors="coerce")
    work = work.dropna(subset=["period", value_col])
    idx = work.groupby("iso3")["period"].idxmax()
    latest = work.loc[idx, ["iso3", "country", "period", value_col]].rename(
        columns={value_col: "value"}
    )
    return latest.reset_index(drop=True)


def fetch_unicef_equity_panel(
    countries: Iterable[str],
    *,
    start_period: int = 2015,
    end_period: int = 2023,
) -> pd.DataFrame:
    """
    Build a country panel from UNICEF indicators for the Fiscal Equity Index demo.

    Requires network access and the ``unicefdata`` package.
    """
    from unicefdata import unicefData

    country_list = list(countries)
    frames: dict[str, pd.DataFrame] = {}

    for col, indicator in UNICEF_EQUITY_INDICATORS.items():
        raw = unicefData(
            indicator=indicator,
            countries=country_list,
            start_period=start_period,
            end_period=end_period,
        )
        latest = _latest_country_values(raw)
        if latest.empty:
            continue
        latest = latest.rename(columns={"value": col})
        frames[col] = latest[["iso3", "country", col]]

    if not frames:
        raise RuntimeError("No UNICEF data returned; check network or country codes.")

    merged = None
    for part in frames.values():
        merged = part if merged is None else merged.merge(part, on=["iso3", "country"], how="outer")

    assert merged is not None
    merged = merged.rename(columns={"country": "entity", "iso3": "country_code"})
    merged["population"] = merged["population"].fillna(merged["population"].median())
    merged["allocated_budget_per_capita"] = merged["allocated_budget_per_capita"].fillna(
        merged["allocated_budget_per_capita"].median()
    )
    merged["health_need_index"] = compute_health_need_index(merged)
    return compute_fiscal_equity_index(merged, entity_col="entity")
