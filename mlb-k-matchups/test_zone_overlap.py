"""Dump-fit tags: pitcher throw pocket × batter swing (no network)."""

from __future__ import annotations

from zone_overlap import (
    classify_dump_fit,
    dump_targets_for_stand,
    attach_dump_fits,
    zone_note_for_batter,
)


def _dump(zone=14, pct=28.0, pitches="ST+KC", out=True):
    return {
        "zone": zone,
        "label": "OUT-DN-1B" if zone == 14 else "HEART",
        "pitcher_pct": pct,
        "out_of_zone": out,
        "pitches": pitches,
    }


def test_dump_targets_picks_top_throw_zones():
    block = {
        "zone_share": {14: 0.32, 12: 0.12, 5: 0.08, 1: 0.05},
        "zone_pitch_mix": {
            14: [{"pitch": "ST", "share": 0.54}, {"pitch": "KC", "share": 0.46}],
            12: [{"pitch": "FF", "share": 0.7}],
        },
    }
    dumps = dump_targets_for_stand(block)
    assert [d["zone"] for d in dumps] == [14, 12]
    assert dumps[0]["pitches"] == "ST+KC"
    assert dumps[0]["out_of_zone"] is True


def test_tunnel_when_dump_is_hot():
    fit = classify_dump_fit(
        [_dump()],
        [{"zone": 14, "swing_pct": 44.0, "whiff_of_swing": 18.0, "xwoba_bip": 0.56}],
        [{"zone": 14, "season_risk": "HOT", "label": "OUT-DN-1B"}],
    )
    assert fit and fit["fit"] == "TUNNEL"


def test_mistake_when_dump_cold_and_heart_hot():
    fit = classify_dump_fit(
        [_dump()],
        [
            {"zone": 14, "swing_pct": 22.0, "whiff_of_swing": 35.0, "xwoba_bip": 0.19},
            {"zone": 5, "swing_pct": 48.0, "whiff_of_swing": 12.0, "xwoba_bip": 0.65},
        ],
        [
            {"zone": 14, "season_risk": "COLD", "label": "OUT-DN-1B"},
            {"zone": 5, "season_risk": "HOT", "label": "HEART"},
        ],
    )
    assert fit and fit["fit"] == "MISTAKE"
    assert "HEART" in fit["mistake_zones"]


def test_chase_high_swing_high_whiff_on_dump():
    fit = classify_dump_fit(
        [_dump()],
        [{"zone": 14, "swing_pct": 48.0, "whiff_of_swing": 36.0, "xwoba_bip": 0.22}],
        [{"zone": 14, "season_risk": "COLD", "label": "OUT-DN-1B"}],
    )
    assert fit and fit["fit"] == "CHASE"


def test_take_low_swing_on_dump():
    fit = classify_dump_fit(
        [_dump()],
        [{"zone": 14, "swing_pct": 18.0, "whiff_of_swing": 20.0, "xwoba_bip": 0.25}],
        [{"zone": 14, "season_risk": "COLD", "label": "OUT-DN-1B"}],
    )
    # Out-of-zone dump + low swing beats COLD damage (not a Hits lean on that pitch).
    assert fit and fit["fit"] == "TAKE"


def test_cold_inzone_dump_without_hot_backup():
    fit = classify_dump_fit(
        [_dump(zone=5, pct=18.0, pitches="FF", out=False)],
        [{"zone": 5, "swing_pct": 52.0, "whiff_of_swing": 12.0, "xwoba_bip": 0.22}],
        [{"zone": 5, "season_risk": "COLD", "label": "HEART"}],
    )
    assert fit and fit["fit"] == "COLD"


def test_dump_targets_accepts_json_string_keys():
    block = {
        "zone_share": {"11": 0.23, "13": 0.21, "5": 0.06},
        "zone_pitch_mix": {
            "11": [{"pitch": "FF", "share": 0.74}, {"pitch": "CH", "share": 0.17}],
            "13": [{"pitch": "CH", "share": 0.55}],
        },
    }
    dumps = dump_targets_for_stand(block)
    assert [d["zone"] for d in dumps] == [11, 13]
    assert dumps[0]["pitches"] == "FF+CH"
    assert dumps[0]["out_of_zone"] is True


def test_offer_swings_dump_without_damage():
    fit = classify_dump_fit(
        [_dump()],
        [{"zone": 14, "swing_pct": 51.0, "whiff_of_swing": 16.0, "xwoba_bip": 0.32}],
        [{"zone": 14, "season_risk": "—", "label": "OUT-DN-1B"}],
    )
    assert fit and fit["fit"] == "OFFER"


def test_attach_dump_fits_on_payload():
    payload = {
        "pitcher": {
            "by_stand": {
                "L": {
                    "zone_share": {14: 0.30, 5: 0.09},
                    "zone_pitch_mix": {14: [{"pitch": "CH", "share": 0.6}]},
                }
            }
        },
        "batters": [
            {
                "name": "Jonathan Aranda",
                "stand": "L",
                "all_zones": [
                    {
                        "zone": 14,
                        "swing_pct": 46.0,
                        "whiff_of_swing": 14.0,
                        "xwoba_bip": 0.56,
                    }
                ],
            }
        ],
        "overlaps": {
            "Jonathan Aranda": [
                {"zone": 14, "season_risk": "HOT", "label": "OUT-DN-1B"}
            ]
        },
    }
    attach_dump_fits(payload)
    assert payload["dump_targets"]["L"][0]["zone"] == 14
    assert payload["batters"][0]["dump_fit"]["fit"] == "TUNNEL"


def test_zone_note_leads_with_dump_fit():
    note = zone_note_for_batter(
        [{"season_risk": "HOT", "label": "HEART", "agreement": "CONFIRM"}],
        dump_fit={"fit": "MISTAKE", "dump_label": "OUT-DN-3B"},
    )
    assert note.startswith("MISTAKE OUT-DN-3B")
    assert "CONFIRM" in note


if __name__ == "__main__":
    test_dump_targets_picks_top_throw_zones()
    test_tunnel_when_dump_is_hot()
    test_mistake_when_dump_cold_and_heart_hot()
    test_chase_high_swing_high_whiff_on_dump()
    test_take_low_swing_on_dump()
    test_cold_inzone_dump_without_hot_backup()
    test_dump_targets_accepts_json_string_keys()
    test_offer_swings_dump_without_damage()
    test_attach_dump_fits_on_payload()
    test_zone_note_leads_with_dump_fit()
    print("ok")
