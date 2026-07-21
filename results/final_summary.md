# hfdata raw vs vwpq final report (v3.6)

Generated: 2026-07-20T16:43:23.336614+00:00

## Split
- IS: 1993–2002
- OOS: 2003–2025

## H1 (primary, common-key ΔRankIC)
- θ̂ = 0.00017976108212005957
- 95% CI = [-0.0019694791946721084, 0.0023432640303719787]
- one-sided 95% lower bound = -0.0016153234351535166
- null_centered p = 0.4371125774845031
- supports positive @5%: False
- bootstrap B=5000 attempts=5000 invalid_rate=0.0

## H2 (economic, gatekept, 10 bps next_open_exec_with_frozen_exit_proxy)
- θ̂ = 0.12793309975866377
- 95% CI = [-0.30940820184322687, 0.7899766694217026]
- one-sided 95% lower bound = -0.21269284122778653
- null_centered p = 0.2605478904219156
- confirmatory (H1 then H2): False
- descriptive only: True

## H3 (raw diagnostic)
- θ̂ = 0.00509028961089313
- supports positive @5%: False

## Units (common-key RankIC)
 I  R   status  rank_ic_raw  rank_ic_vwpq  delta_rank_ic  n_common  n_dates  n_raw  n_vwpq  ensemble_n_equal  rankic_n_raw  rankic_n_vwpq  rankic_uses_n_common_only  common_key_equal_n                                                                                                                                                          common_key_equal_n_note
 5  5 complete     0.008333      0.008606       0.000273    425670      487 425670 1158046             False        425670         425670                       True                True RankIC Δ uses n_common only (raw∩vwpq); common_key_equal_n reflects rankic_n_raw==rankic_n_vwpq==n_common; ensemble_n_equal is separate (may be False when partial images exist)
 5 20 complete    -0.005578     -0.000570       0.005007     99000       98  99000  113929             False         99000          99000                       True                True RankIC Δ uses n_common only (raw∩vwpq); common_key_equal_n reflects rankic_n_raw==rankic_n_vwpq==n_common; ensemble_n_equal is separate (may be False when partial images exist)
 5 60 complete    -0.004308      0.001879       0.006186     30947       30  30947   32001             False         30947          30947                       True                True RankIC Δ uses n_common only (raw∩vwpq); common_key_equal_n reflects rankic_n_raw==rankic_n_vwpq==n_common; ensemble_n_equal is separate (may be False when partial images exist)
20  5 complete    -0.015634     -0.013986       0.001649    113929      112 113929  113929              True        113929         113929                       True                True RankIC Δ uses n_common only (raw∩vwpq); common_key_equal_n reflects rankic_n_raw==rankic_n_vwpq==n_common; ensemble_n_equal is separate (may be False when partial images exist)
20 20 complete     0.001745     -0.004723      -0.006468    270788      263 270788  270788              True        270788         270788                       True                True RankIC Δ uses n_common only (raw∩vwpq); common_key_equal_n reflects rankic_n_raw==rankic_n_vwpq==n_common; ensemble_n_equal is separate (may be False when partial images exist)
20 60 complete     0.006594      0.003658      -0.002936     89006       87  89006   89006              True         89006          89006                       True                True RankIC Δ uses n_common only (raw∩vwpq); common_key_equal_n reflects rankic_n_raw==rankic_n_vwpq==n_common; ensemble_n_equal is separate (may be False when partial images exist)
60  5 complete     0.027240      0.022355      -0.004885     32001       31  32001   32001              True         32001          32001                       True                True RankIC Δ uses n_common only (raw∩vwpq); common_key_equal_n reflects rankic_n_raw==rankic_n_vwpq==n_common; ensemble_n_equal is separate (may be False when partial images exist)
60 20 complete     0.009345      0.011270       0.001925     89006       87  89006   89006              True         89006          89006                       True                True RankIC Δ uses n_common only (raw∩vwpq); common_key_equal_n reflects rankic_n_raw==rankic_n_vwpq==n_common; ensemble_n_equal is separate (may be False when partial images exist)
60 60 complete     0.018075      0.018943       0.000868     89876       87  89876   89876              True         89876          89876                       True                True RankIC Δ uses n_common only (raw∩vwpq); common_key_equal_n reflects rankic_n_raw==rankic_n_vwpq==n_common; ensemble_n_equal is separate (may be False when partial images exist)

## Exit-proxy coverage (diagonal)
{
  "i5_r5_raw": {
    "n_cohorts": 487,
    "n_formable": 487,
    "n_leg_empty": 51,
    "n_attempted_entries": 84672,
    "exact_entry_fill_rate": 0.8918650793650794,
    "entry_unfilled_rate": 0.10813492063492064,
    "n_exact_exit": 67019,
    "n_proxy_exit": 8497,
    "proxy_exit_share": 0.11251920122887865,
    "endpoint": "next_open_exec_with_frozen_exit_proxy",
    "primary_cost_bps": 10,
    "K_R": 1,
    "n_common_scored_keys": 425670
  },
  "i5_r5_vwpq": {
    "n_cohorts": 487,
    "n_formable": 487,
    "n_leg_empty": 51,
    "n_attempted_entries": 84672,
    "exact_entry_fill_rate": 0.891380857898715,
    "entry_unfilled_rate": 0.10861914210128495,
    "n_exact_exit": 66942,
    "n_proxy_exit": 8533,
    "proxy_exit_share": 0.11305730374296125,
    "endpoint": "next_open_exec_with_frozen_exit_proxy",
    "primary_cost_bps": 10,
    "K_R": 1,
    "n_common_scored_keys": 425670
  },
  "i20_r20_raw": {
    "n_cohorts": 263,
    "n_formable": 263,
    "n_leg_empty": 29,
    "n_attempted_entries": 53910,
    "exact_entry_fill_rate": 0.8852531997774068,
    "entry_unfilled_rate": 0.11474680022259322,
    "n_exact_exit": 44924,
    "n_proxy_exit": 2800,
    "proxy_exit_share": 0.0586706897996815,
    "endpoint": "next_open_exec_with_frozen_exit_proxy",
    "primary_cost_bps": 10,
    "K_R": 1,
    "n_common_scored_keys": 270788
  },
  "i20_r20_vwpq": {
    "n_cohorts": 263,
    "n_formable": 263,
    "n_leg_empty": 29,
    "n_attempted_entries": 53910,
    "exact_entry_fill_rate": 0.8851419031719533,
    "entry_unfilled_rate": 0.11485809682804675,
    "n_exact_exit": 44906,
    "n_proxy_exit": 2812,
    "proxy_exit_share": 0.05892954440672283,
    "endpoint": "next_open_exec_with_frozen_exit_proxy",
    "primary_cost_bps": 10,
    "K_R": 1,
    "n_common_scored_keys": 270788
  },
  "i60_r60_raw": {
    "n_cohorts": 87,
    "n_formable": 87,
    "n_leg_empty": 19,
    "n_attempted_entries": 17898,
    "exact_entry_fill_rate": 0.7723209297128171,
    "entry_unfilled_rate": 0.22767907028718293,
    "n_exact_exit": 11773,
    "n_proxy_exit": 2050,
    "proxy_exit_share": 0.1483035520509296,
    "endpoint": "next_open_exec_with_frozen_exit_proxy",
    "primary_cost_bps": 10,
    "K_R": 1,
    "n_common_scored_keys": 89876
  },
  "i60_r60_vwpq": {
    "n_cohorts": 87,
    "n_formable": 87,
    "n_leg_empty": 19,
    "n_attempted_entries": 17898,
    "exact_entry_fill_rate": 0.7727120348642307,
    "entry_unfilled_rate": 0.22728796513576935,
    "n_exact_exit": 11782,
    "n_proxy_exit": 2048,
    "proxy_exit_share": 0.14808387563268258,
    "endpoint": "next_open_exec_with_frozen_exit_proxy",
    "primary_cost_bps": 10,
    "K_R": 1,
    "n_common_scored_keys": 89876
  }
}

Endpoint: next_open_exec_with_frozen_exit_proxy; costs one-way 10 bps primary; Sharpe √252.
Does not claim official CRSP/Jiang absolute metric reproduction.
