#!/usr/bin/env python3
"""Analytical Poisson prize-sharing illustration, NOT calibrated to actual Vietlott ticket sales."""
import json,math
from pathlib import Path
out=Path(__file__).resolve().parent/"anticrowd_scenarios.json"
N=math.comb(55,6);tickets=6
p=tickets/N
scenarios=[]
for lam in (0.05,0.2,0.5,1.0,2.0):
    retention=-math.expm1(-lam)/lam
    scenarios.append({"mean_other_holders":lam,
        "prob_at_least_one_other_holder":-math.expm1(-lam),
        "expected_share_if_jackpot":retention,
        "example_share_100b_vnd":100_000_000_000*retention,
        "example_unconditional_jackpot_component_six_tickets_vnd":p*100_000_000_000*retention})
result={"assumption":"hypothetical: other holders of each specific ticket follow Poisson(lambda), uniform fair draw; all six tickets distinct; 100 billion VND Jackpot pool",
 "jackpot_combinations":N,"six_ticket_jackpot_probability":p,
 "one_in_draws":N/tickets,"scenarios":scenarios,
 "warning":"The lambda values are arbitrary illustrative assumptions; historical prize-tier ratios do not identify exact ticket-copy frequencies. No increase in the chance of Jackpot is implied."}
out.write_text(json.dumps(result,indent=2)+"\n")
print("RESULT_JSON="+json.dumps(result))
