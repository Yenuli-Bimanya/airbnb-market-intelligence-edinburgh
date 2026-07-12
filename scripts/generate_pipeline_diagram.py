"""Generate Figure 1: end-to-end pipeline architecture for the PDF report."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUTPUT = Path(__file__).resolve().parents[1] / "reports" / "figures" / "00_pipeline_architecture.png"

# Layout: (x, y, width, height, label, color)
BOXES = [
    (0.5, 0.88, 0.9, 0.07, "Inside Airbnb Raw Files\n(CSV / GeoJSON / gzip)", "#E8F4FD"),
    (0.5, 0.76, 0.9, 0.06, "Extract — src/extract_files.py\n→ data/interim/edinburgh/2026-06-23/", "#D6EAF8"),
    (0.5, 0.66, 0.9, 0.06, "Profile — src/profile_datasets.py\n→ data/metadata/", "#D6EAF8"),
    (0.5, 0.56, 0.9, 0.06, "Clean — src/cleaning.py\n→ *_clean.parquet", "#D5F5E3"),
    (0.5, 0.46, 0.9, 0.06, "Validate — src/validation.py\n→ *_validated.parquet + validation_report.csv", "#D5F5E3"),
    (0.5, 0.36, 0.9, 0.06, "Enrich — src/transformations.py\n→ listings_enriched.parquet", "#FCF3CF"),
    (0.5, 0.26, 0.9, 0.06, "Warehouse — src/database.py + sql/create_*.sql\n→ database/airbnb.duckdb (DuckDB star schema)", "#FADBD8"),
    (0.28, 0.14, 0.38, 0.07, "Analytics Notebooks\nEDA · Stats · ML · NLP\n→ reports/figures + reports/tables", "#E8DAEF"),
    (0.72, 0.14, 0.38, 0.07, "Dashboard — dashboard/app.py\nPlotly Dash (interactive UI)", "#E8DAEF"),
]

ARROWS = [
    (0.5, 0.85, 0.5, 0.82),
    (0.5, 0.73, 0.5, 0.69),
    (0.5, 0.63, 0.5, 0.59),
    (0.5, 0.53, 0.5, 0.49),
    (0.5, 0.43, 0.5, 0.39),
    (0.5, 0.33, 0.5, 0.29),
    (0.5, 0.23, 0.28, 0.21),
    (0.5, 0.23, 0.72, 0.21),
]

ORCHESTRATION = (
    "Orchestration: python -m src.pipeline  |  "
    "Config: config/config.yaml via src/config.py"
)


def main() -> None:
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    for x, y, w, h, label, color in BOXES:
        box = FancyBboxPatch(
            (x - w / 2, y - h / 2),
            w,
            h,
            boxstyle="round,pad=0.01,rounding_size=0.015",
            linewidth=1.2,
            edgecolor="#2C3E50",
            facecolor=color,
            transform=ax.transData,
            zorder=2,
        )
        ax.add_patch(box)
        ax.text(
            x,
            y,
            label,
            ha="center",
            va="center",
            fontsize=9.5,
            color="#1A1A2E",
            linespacing=1.35,
            zorder=3,
        )

    for x1, y1, x2, y2 in ARROWS:
        ax.annotate(
            "",
            xy=(x2, y2),
            xytext=(x1, y1),
            arrowprops=dict(arrowstyle="-|>", color="#2C3E50", lw=1.5, shrinkA=2, shrinkB=2),
            zorder=1,
        )

    ax.text(
        0.5,
        0.97,
        "Figure 1. End-to-End Data Pipeline Architecture",
        ha="center",
        va="center",
        fontsize=14,
        fontweight="bold",
        color="#1B2A4A",
    )
    ax.text(
        0.5,
        0.03,
        ORCHESTRATION,
        ha="center",
        va="center",
        fontsize=9,
        color="#566573",
        style="italic",
    )

    fig.patch.set_facecolor("white")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    main()
