"""Illustrative sample-size calculation, not an empirical lottery result."""
import json
import math
from pathlib import Path
from statistics import NormalDist
ROOT=Path(__file__).resolve().parents[1]


def main():
    p0=6/55;alpha=.05;family=55;power=.8;n=20
    zcrit=NormalDist().inv_cdf(1-alpha/(2*family));zpower=NormalDist().inv_cdf(power)
    rows=[]
    for relative in [.05,.10,.20]:
        p1=p0*(1+relative);delta=p1-p0
        required=math.ceil((zcrit*math.sqrt(p0*(1-p0))+zpower*math.sqrt(p1*(1-p1)))**2/delta**2)
        rows.append({'relative_inclusion_increase':relative,'alternative_probability':p1,
                     'approx_independent_draws_for_80pct_power':required})
    r={'status':'theoretical_illustration_only','null_main_inclusion_probability':p0,
       'baseline_draws':n,'expected_inclusions_per_label_at20':n*p0,
       'binomial_standard_error_at20':math.sqrt(p0*(1-p0)/n),'family':family,'FWER_alpha':alpha,
       'approximation':'Two-sided Bonferroni normal approximation for one Bernoulli marginal, power .8; assumes independent identical draws and known null.',
       'formula':'N = (z_(1-alpha/(2*55))*sqrt(p0*(1-p0)) + z_.8*sqrt(p1*(1-p1)))^2 / (p1-p0)^2',
       'scenarios':rows,'limitations':['Not a design for clustered machine/ball-set changes, model selection or multiple stages.',
          'Mechanical observability and independent real validation are required even with more simulated seeds.',
          'No estimate of actual Vietlott bias, no forecast and no claim that these draw counts establish an edge.']}
    (ROOT/'results/power_planning.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))

if __name__=='__main__':main()
