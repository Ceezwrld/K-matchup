"""Order-walk expected hits / RBI traffic (no network)."""

from __future__ import annotations

from sharpen import (
    attach_lineup_expected_hits,
    pa_hit_probability,
    rbi_spot_label,
    _binomial_p_ge,
)


def _batter(
    slot: int,
    name: str,
    *,
    k_pct: float = 22.0,
    avg: float = 0.270,
    xba: float = 0.260,
    bb: float = 8.0,
    hits_score: float = 55.0,
    hr_rbi: float = 54.0,
    barrel: float = 8.0,
    expected_ks: float = 4.38,
) -> dict:
    return {
        "slot": slot,
        "batter": name,
        "batter_id": 1000 + slot,
        "status": "ok",
        "expected_k_pct": k_pct,
        "expected_ks": expected_ks,
        "avg_vs_hand": avg,
        "xba": xba,
        "bb_pct": bb,
        "hits_score": hits_score,
        "hr_rbi_score": hr_rbi,
        "barrel_pct": barrel,
    }


def test_21_bf_gives_3_pa_to_top_three_and_2_to_rest():
    nine = [_batter(i, f"B{i}") for i in range(1, 10)]
    attach_lineup_expected_hits(nine, projected_bf=21, pitcher_xba=0.250)
    by_slot = {int(b["slot"]): b for b in nine}
    assert [by_slot[i]["pa_vs_sp"] for i in range(1, 10)] == [3, 3, 3, 2, 2, 2, 2, 2, 2]


def test_same_p_more_pa_raises_p_ge_1():
    nine = [_batter(i, f"B{i}", k_pct=20.0, avg=0.300) for i in range(1, 10)]
    attach_lineup_expected_hits(nine, projected_bf=21, pitcher_xba=0.250)
    lead = next(b for b in nine if b["slot"] == 1)
    four = next(b for b in nine if b["slot"] == 4)
    assert lead["p_hit"] == four["p_hit"]
    assert lead["p_ge_1"] > four["p_ge_1"]
    assert lead["expected_hits"] > four["expected_hits"]


def test_cleanup_rbi_spot_beats_leadoff_with_weak_bottom():
    nine = []
    for i in range(1, 10):
        # Bottom of order is weak OBP; 2–3 are on-base machines.
        avg = 0.320 if i in (2, 3) else (0.210 if i >= 8 else 0.260)
        bb = 12.0 if i in (2, 3) else 6.0
        nine.append(_batter(i, f"B{i}", avg=avg, bb=bb, hr_rbi=62.0 if i == 4 else 50.0))
    attach_lineup_expected_hits(nine, projected_bf=21, pitcher_xba=0.250)
    lead = next(b for b in nine if b["slot"] == 1)
    clean = next(b for b in nine if b["slot"] == 4)
    assert clean["p_man_on"] > lead["p_man_on"]
    assert clean["rbi_spot_score"] > lead["rbi_spot_score"]
    assert clean["rbi_spot"] in {"good", "prime"}
    assert lead["rbi_spot"] == "thin"


def test_soft_contact_pitcher_raises_p_hit_vs_whiff_arm():
    low = pa_hit_probability(
        expected_k_pct=20.0,
        bb_pct=8.0,
        batter_avg=0.280,
        batter_xba=0.270,
        pitcher_xba=0.175,
        pitcher_ba_against=0.160,
    )
    high = pa_hit_probability(
        expected_k_pct=20.0,
        bb_pct=8.0,
        batter_avg=0.280,
        batter_xba=0.270,
        pitcher_xba=0.265,
        pitcher_ba_against=0.250,
    )
    assert high > low


def test_does_not_rewrite_k_or_talent_scores():
    nine = [_batter(i, f"B{i}", expected_ks=4.38, hits_score=59.5) for i in range(1, 10)]
    attach_lineup_expected_hits(nine, projected_bf=21, pitcher_xba=0.174, pitcher_style="whiff")
    for b in nine:
        assert b["expected_ks"] == 4.38
        assert b["expected_k_pct"] == 22.0
        assert b["hits_score"] == 59.5
        assert b["hits_env"] == "k_arm"


def test_p_ge_2_zero_when_one_pa():
    one = [_batter(1, "Solo")]
    attach_lineup_expected_hits(one, projected_bf=1, pitcher_xba=0.250)
    assert one[0]["pa_vs_sp"] == 1
    assert one[0]["p_ge_2"] == 0.0
    assert 0.0 < one[0]["p_ge_1"] < 1.0


def test_binomial_ge_matches_closed_form():
    p = 0.27
    n = 3
    q = 1 - p
    assert abs(_binomial_p_ge(n, p, 1) - (1 - q**n)) < 1e-12
    assert abs(_binomial_p_ge(n, p, 2) - (1 - q**n - n * p * q ** (n - 1))) < 1e-12


def test_rbi_spot_thresholds():
    assert rbi_spot_label(61) == "prime"
    assert rbi_spot_label(50) == "good"
    assert rbi_spot_label(49.9) == "thin"
    assert rbi_spot_label(None) is None


if __name__ == "__main__":
    test_21_bf_gives_3_pa_to_top_three_and_2_to_rest()
    test_same_p_more_pa_raises_p_ge_1()
    test_cleanup_rbi_spot_beats_leadoff_with_weak_bottom()
    test_soft_contact_pitcher_raises_p_hit_vs_whiff_arm()
    test_does_not_rewrite_k_or_talent_scores()
    test_p_ge_2_zero_when_one_pa()
    test_binomial_ge_matches_closed_form()
    test_rbi_spot_thresholds()
    print("ok")
