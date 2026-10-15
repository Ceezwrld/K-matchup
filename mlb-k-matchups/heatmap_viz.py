"""Visual zone heatmaps (catcher's view) for pitcher location vs batter damage.

Produces PNG images + a small HTML gallery. Display-only — does not change
``expected_ks`` or hits scores.

Layout (Savant zones, catcher's view)::

        11          12
     1    2    3
     4    5    6
     7    8    9
        13          14

For RHB: zones 1/4/7 ≈ inside (3B). For LHB: 3/6/9 ≈ inside (1B).
"""

from __future__ import annotations

import html
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np

# Catcher's-view grid positions (col, row) — row 0 = top
ZONE_POS: dict[int, tuple[int, int]] = {
    11: (0, 0),
    12: (2, 0),
    1: (0, 1),
    2: (1, 1),
    3: (2, 1),
    4: (0, 2),
    5: (1, 2),
    6: (2, 2),
    7: (0, 3),
    8: (1, 3),
    9: (2, 3),
    13: (0, 4),
    14: (2, 4),
}

ZONE_SHORT = {
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    11: "11",
    12: "12",
    13: "13",
    14: "14",
}


def _values_to_grid(values: dict[int, float]) -> np.ndarray:
    """3 cols × 5 rows; missing cells = nan."""
    grid = np.full((5, 3), np.nan, dtype=float)
    for z, (c, r) in ZONE_POS.items():
        if z in values:
            grid[r, c] = float(values[z])
    return grid


def _draw_plate_grid(
    ax: Any,
    grid: np.ndarray,
    *,
    cmap: str,
    vmin: float | None,
    vmax: float | None,
    title: str,
    fmt: str,
    annotations: dict[int, str] | None = None,
    risk_outline: dict[int, str] | None = None,
) -> Any:
    ax.set_xlim(-0.05, 3.05)
    ax.set_ylim(5.05, -0.05)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title, fontsize=11, pad=8, fontweight="bold")

    cmap_obj = plt.get_cmap(cmap)
    norm = mcolors.Normalize(
        vmin=vmin if vmin is not None else float(np.nanmin(grid)),
        vmax=vmax if vmax is not None else float(np.nanmax(grid)),
    )

    risk_colors = {"HOT": "#c62828", "WARM": "#ef6c00", "COLD": "#1565c0"}

    for z, (c, r) in ZONE_POS.items():
        val = grid[r, c]
        if np.isnan(val):
            face = "#eceff1"
        else:
            face = cmap_obj(norm(val))
        # Strike zone cells slightly larger border
        in_zone = z <= 9
        rect = FancyBboxPatch(
            (c + 0.06, r + 0.06),
            0.88,
            0.88,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            linewidth=2.2 if in_zone else 1.0,
            edgecolor="#263238" if in_zone else "#90a4ae",
            facecolor=face,
        )
        ax.add_patch(rect)
        label = ZONE_SHORT[z]
        ax.text(
            c + 0.5,
            r + 0.32,
            label,
            ha="center",
            va="center",
            fontsize=8,
            color="#37474f",
            alpha=0.7,
        )
        if not np.isnan(val):
            ax.text(
                c + 0.5,
                r + 0.58,
                fmt.format(val),
                ha="center",
                va="center",
                fontsize=9,
                fontweight="700",
                color="#102027",
            )
        if annotations and z in annotations:
            ax.text(
                c + 0.5,
                r + 0.82,
                annotations[z],
                ha="center",
                va="center",
                fontsize=7,
                color="#102027",
            )
        if risk_outline and z in risk_outline:
            risk = risk_outline[z]
            outline = Rectangle(
                (c + 0.02, r + 0.02),
                0.96,
                0.96,
                fill=False,
                linewidth=3.0,
                edgecolor=risk_colors.get(risk, "#000"),
            )
            ax.add_patch(outline)

    # Home plate cue under zone
    ax.text(1.5, 4.85, "▲ plate (catcher's view)", ha="center", fontsize=8, color="#607d8b")
    return norm


def render_pitcher_location_png(
    zone_share: dict[int, float],
    *,
    title: str,
    path: Path,
    stand_label: str = "",
) -> Path:
    """zone_share values are fractions (0–1)."""
    vals = {int(k): float(v) * 100 for k, v in zone_share.items()}
    grid = _values_to_grid(vals)
    fig, ax = plt.subplots(figsize=(4.2, 6.2), dpi=140)
    _draw_plate_grid(
        ax,
        grid,
        cmap="Blues",
        vmin=0,
        vmax=max(35.0, float(np.nanmax(grid)) if np.isfinite(grid).any() else 20),
        title=f"{title}\nthrows % {stand_label}".strip(),
        fmt="{:.0f}%",
    )
    fig.tight_layout()
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def render_batter_damage_png(
    zone_xwoba: dict[int, float],
    *,
    title: str,
    path: Path,
    swing_pct: dict[int, float] | None = None,
    risk_outline: dict[int, str] | None = None,
) -> Path:
    vals = {int(k): float(v) for k, v in zone_xwoba.items()}
    grid = _values_to_grid(vals)
    ann = None
    if swing_pct:
        ann = {z: f"sw {swing_pct[z]:.0f}%" for z in swing_pct if z in vals}
    fig, ax = plt.subplots(figsize=(4.2, 6.2), dpi=140)
    _draw_plate_grid(
        ax,
        grid,
        cmap="RdYlGn",
        vmin=0.20,
        vmax=0.55,
        title=f"{title}\ndamage xwOBA (BIP)",
        fmt="{:.3f}",
        annotations=ann,
        risk_outline=risk_outline,
    )
    fig.tight_layout()
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def render_overlap_png(
    zone_share: dict[int, float],
    zone_xwoba: dict[int, float],
    *,
    title: str,
    path: Path,
    risk_by_zone: dict[int, str] | None = None,
) -> Path:
    """Combined view: cell color = batter xwOBA; label includes pitcher %."""
    dmg = {int(k): float(v) for k, v in zone_xwoba.items()}
    share = {int(k): float(v) * 100 for k, v in zone_share.items()}
    grid = _values_to_grid(dmg)
    ann = {
        z: f"W {share[z]:.0f}%"
        for z in set(dmg) | set(share)
        if z in share
    }
    fig, ax = plt.subplots(figsize=(4.4, 6.4), dpi=140)
    _draw_plate_grid(
        ax,
        grid,
        cmap="RdYlGn",
        vmin=0.20,
        vmax=0.55,
        title=f"{title}\noverlap (color=damage, W%=throws)",
        fmt="{:.3f}",
        annotations=ann,
        risk_outline=risk_by_zone,
    )
    fig.tight_layout()
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def write_gallery_html(
    *,
    out_path: Path,
    pitcher_name: str,
    game: str | None,
    cards: list[dict[str, str]],
) -> Path:
    """cards: {batter, pitcher_img, batter_img, overlap_img, note}."""
    parts = [
        "<!DOCTYPE html><html><head><meta charset='utf-8'/>",
        f"<title>Zone maps — {html.escape(pitcher_name)}</title>",
        "<style>",
        "body{font-family:system-ui,sans-serif;background:#0f1419;color:#e7ecf1;margin:0;padding:24px}",
        "h1{font-size:1.4rem;margin:0 0 4px} .sub{color:#9aa7b5;margin:0 0 20px}",
        ".grid{display:grid;gap:20px}",
        ".card{background:#1a222c;border-radius:12px;padding:16px}",
        ".card h2{margin:0 0 10px;font-size:1.05rem}",
        ".imgs{display:flex;flex-wrap:wrap;gap:12px}",
        ".imgs figure{margin:0;text-align:center}",
        ".imgs img{max-width:220px;width:100%;border-radius:8px;background:#fff}",
        ".imgs figcaption{font-size:0.75rem;color:#9aa7b5;margin-top:4px}",
        ".note{font-size:0.85rem;color:#c5d0da;margin-top:10px}",
        ".legend span{display:inline-block;margin-right:12px;font-size:0.8rem}",
        ".hot{color:#ef5350}.warm{color:#ffa726}.cold{color:#42a5f5}",
        "</style></head><body>",
        f"<h1>Zone heatmaps — {html.escape(pitcher_name)}</h1>",
        f"<p class='sub'>{html.escape(game or '')} · catcher view · red outline=HOT · blue=COLD</p>",
        "<p class='legend'><span class='hot'>HOT</span><span class='warm'>WARM</span>"
        "<span class='cold'>COLD</span> · color on batter/overlap = xwOBA damage</p>",
        "<div class='grid'>",
    ]
    for c in cards:
        parts.append("<div class='card'>")
        parts.append(f"<h2>{html.escape(c['batter'])}</h2>")
        parts.append("<div class='imgs'>")
        for key, cap in (
            ("pitcher_img", "Pitcher throws %"),
            ("batter_img", "Batter damage"),
            ("overlap_img", "Overlap"),
        ):
            if c.get(key):
                parts.append(
                    f"<figure><img src='{html.escape(c[key])}' alt='{cap}'/>"
                    f"<figcaption>{cap}</figcaption></figure>"
                )
        parts.append("</div>")
        if c.get("note"):
            parts.append(f"<p class='note'>{html.escape(c['note'])}</p>")
        parts.append("</div>")
    parts.append("</div></body></html>")
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(parts))
    return out_path


def build_images_from_payload(
    payload: dict[str, Any],
    *,
    out_dir: Path,
) -> dict[str, Any]:
    """Render PNGs + gallery from a zone_overlap JSON payload."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    pitcher = payload.get("pitcher") or {}
    pname = str(pitcher.get("name") or "pitcher")
    game = pitcher.get("game")
    by_stand = pitcher.get("by_stand") or {}
    overlaps = payload.get("overlaps") or {}
    cards: list[dict[str, str]] = []
    manifest: list[dict[str, Any]] = []

    for b in payload.get("batters") or []:
        name = str(b.get("name"))
        stand = str(b.get("stand") or "R")
        block = by_stand.get(stand) or {}
        share = {int(k): float(v) for k, v in (block.get("zone_share") or {}).items()}
        zone_xw: dict[int, float] = {}
        swing: dict[int, float] = {}
        for row in b.get("all_zones") or []:
            z = int(row["zone"])
            if row.get("xwoba_bip") is not None:
                zone_xw[z] = float(row["xwoba_bip"])
            if row.get("swing_pct") is not None:
                swing[z] = float(row["swing_pct"])
        risk_map: dict[int, str] = {}
        notes = []
        for ov in overlaps.get(name) or []:
            if ov.get("risk") in ("HOT", "WARM", "COLD"):
                risk_map[int(ov["zone"])] = ov["risk"]
                if ov["risk"] in ("HOT", "COLD"):
                    notes.append(f"{ov['risk']} {ov['label']}")

        # ASCII-fold so accents (Díaz, José) don't break paths / previews
        import unicodedata

        folded = unicodedata.normalize("NFKD", name.lower())
        folded = "".join(ch for ch in folded if not unicodedata.combining(ch))
        slug = "".join(ch if ch.isalnum() else "-" for ch in folded).strip("-")
        slug = "-".join(p for p in slug.split("-") if p)
        p_img = out_dir / f"{slug}-pitcher-vs{stand}.png"
        b_img = out_dir / f"{slug}-batter-damage.png"
        o_img = out_dir / f"{slug}-overlap.png"

        render_pitcher_location_png(
            share,
            title=f"{pname}",
            path=p_img,
            stand_label=f"vs {stand}HB",
        )
        render_batter_damage_png(
            zone_xw,
            title=name,
            path=b_img,
            swing_pct=swing,
            risk_outline=risk_map,
        )
        render_overlap_png(
            share,
            zone_xw,
            title=f"{name} vs {pname}",
            path=o_img,
            risk_by_zone=risk_map,
        )
        note = " · ".join(notes[:4]) if notes else ""
        cards.append(
            {
                "batter": name,
                "pitcher_img": p_img.name,
                "batter_img": b_img.name,
                "overlap_img": o_img.name,
                "note": note,
            }
        )
        manifest.append(
            {
                "batter": name,
                "stand": stand,
                "pitcher_img": str(p_img),
                "batter_img": str(b_img),
                "overlap_img": str(o_img),
                "note": note,
            }
        )

    gallery = write_gallery_html(
        out_path=out_dir / "index.html",
        pitcher_name=pname,
        game=str(game) if game else None,
        cards=cards,
    )
    return {"gallery": str(gallery), "cards": manifest, "dir": str(out_dir)}
