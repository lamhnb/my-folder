#!/usr/bin/env python3
"""Champion-X: player-number preferences from prize-tier counts, research only.
Fetches public Power 6/55 results. Never modifies Frozen code or predicts balls.
"""
import csv, hashlib, io, json, math, random, statistics, urllib.request
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
OUT = BASE / "jackpot_player_choice_outputs"
OUT.mkdir(parents=True, exist_ok=True)
MAIN = "https://raw.githubusercontent.com/vietvudanh/vietlott-data/main/data/power655.jsonl"
PRIZES = "https://raw.githubusercontent.com/leoodz/vn-vietlott/main/results/power6x55.json"
def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent":"Champion-X-research/1.0"})
    with urllib.request.urlopen(req, timeout=45) as r: return r.read()
def count(value):
    if isinstance(value, dict): value=value.get("count")
    if value is None or isinstance(value, bool): return None
    try: return int(str(value).replace(",","").replace(".","").strip())
    except (ValueError, TypeError): return None
def amount(value):
    if isinstance(value, dict): value=value.get("amount")
    return count(str(value or "").replace("đ","").replace("₫","").replace(" ",""))
def corr(x,y):
    if len(x)<4: return None
    mx=sum(x)/len(x);my=sum(y)/len(y)
    xx=sum((a-mx)**2 for a in x);yy=sum((b-my)**2 for b in y)
    return sum((a-mx)*(b-my) for a,b in zip(x,y))/math.sqrt(xx*yy) if xx>0 and yy>0 else None
def feature(nums):
    s=sorted(nums)
    return {"low31":sum(n<=31 for n in s),"high40":sum(n>=40 for n in s),
            "sum":sum(s),"adjacent":sum(s[i+1]-s[i]==1 for i in range(5)),
            "odd":sum(n%2 for n in s),"span":s[-1]-s[0]}
raw=fetch(MAIN);pr=fetch(PRIZES)
draws=[json.loads(s) for s in raw.decode().splitlines() if s.strip()]
details=json.loads(pr)
assert isinstance(details,list), "Unexpected prize source schema"
draw_by_date=defaultdict(list)
for row in draws:
    try:
        dt=datetime.strptime(row["date"],"%Y-%m-%d").date()
        nums=[int(x) for x in row["result"][:6]]
        assert len(nums)==6 and len(set(nums))==6 and all(1<=x<=55 for x in nums)
        draw_by_date[dt].append(row)
    except (KeyError,ValueError,AssertionError,TypeError): continue
usable=[];reasons=Counter();seen=set()
for item in details:
    try:
        dt=datetime.strptime(item["date"],"%d-%m-%Y").date()
        nums=sorted(int(n) for n in item["numbers"])
        if len(nums)!=6 or len(set(nums))!=6: raise ValueError("invalid numbers")
        matching=[d for d in draw_by_date.get(dt,[]) if sorted(d["result"][:6])==nums]
        if len(matching)!=1: raise ValueError("draw alignment not unique")
        if dt in seen: raise ValueError("duplicate date")
        prizes=item["prizes"]
        n3=count(prizes.get("giai_ba"));n4=count(prizes.get("giai_nhi"))
        n5=count(prizes.get("giai_nhat"));jp=count(prizes.get("jackpot1"))
        jackpot=amount(prizes.get("jackpot1"))
        if n3 is None or n3<=0 or n4 is None or n5 is None or jp is None:
            raise ValueError("missing/bogus prize counts")
        if not (0<=n5<=n4<=n3): raise ValueError("inconsistent tier counts")
        if jackpot is None or jackpot<=0: raise ValueError("bad jackpot amount")
        features=feature(nums)
        row={"date":dt.isoformat(),"id":matching[0]["id"],"year":dt.year,
             "numbers":" ".join(f"{n:02d}" for n in nums),"bonus":matching[0]["result"][6],
             "n3":n3,"n4":n4,"n5":n5,"jackpot1_count":jp,"jackpot1_amount_vnd":jackpot,
             **features}
        usable.append(row);seen.add(dt)
    except (KeyError,ValueError,TypeError,IndexError) as e: reasons[str(e)]+=1
usable.sort(key=lambda x:(x["date"],int(x["id"])))
D=math.comb(55,6);p3=math.comb(6,3)*math.comb(49,3)/D
p4=math.comb(6,4)*math.comb(49,2)/D;p5=6*48/D
for r in usable:
    r["sales_equivalent_from_n3"]=r["n3"]/p3
    r["ratio4_vs_uniform"]=(r["n4"]/r["n3"])/(p4/p3)
    r["ratio5_vs_uniform"]=(r["n5"]/r["n3"])/(p5/p3)
    r["jackpot_won"]=int(r["jackpot1_count"]>0)
    r["high_low_group"]=int(r["low31"]>=4)
def average(rows,key): return sum(r[key] for r in rows)/len(rows) if rows else None
def year_adjusted_corr(rows,x,y):
    groups=defaultdict(list)
    for r in rows: groups[r["year"]].append(r)
    xx=[r[x]-average(groups[r["year"]],x) for r in rows]
    yy=[r[y]-average(groups[r["year"]],y) for r in rows]
    return corr(xx,yy)
groups=defaultdict(list)
for r in usable: groups[r["year"]].append(r)
features=["low31","high40","sum","adjacent","odd","span"]
metrics=["jackpot_won","ratio4_vs_uniform","ratio5_vs_uniform","sales_equivalent_from_n3"]
associations={}
for m in metrics:
    associations[m]={}
    for f in features:
        associations[m][f]={"pearson":corr([r[f] for r in usable],[r[m] for r in usable]),
                            "year_adjusted":year_adjusted_corr(usable,f,m)}
# Year-stratified shuffling of Jackpot-claim labels (exploratory, no sales controls).
seed=20261103;rng=random.Random(seed);B=3000;obs=year_adjusted_corr(usable,"low31","jackpot_won")
ge=0
for _ in range(B):
    shuffled=[]
    for year,items in groups.items():
        perm=[r["jackpot_won"] for r in items];rng.shuffle(perm)
        shuffled.extend([{**r,"jackpot_won":v} for r,v in zip(items,perm)])
    z=year_adjusted_corr(shuffled,"low31","jackpot_won")
    if obs is not None and z is not None and abs(z)>=abs(obs): ge+=1
p=(ge+1)/(B+1) if obs is not None else None
kpis={"main_source_sha256":hashlib.sha256(raw).hexdigest(),
      "prize_source_sha256":hashlib.sha256(pr).hexdigest(),
      "raw_draws":len(draws),"raw_prize_rows":len(details),
      "matched_valid":len(usable),"rejected_reasons":dict(reasons),
      "jackpot1_winning_draws":sum(r["jackpot_won"] for r in usable),
      "theoretical_p3":p3,"theoretical_p4_over_p3":p4/p3,
      "theoretical_p5_over_p3":p5/p3,
      "mean_ratio4":average(usable,"ratio4_vs_uniform"),
      "mean_ratio5":average(usable,"ratio5_vs_uniform"),
      "year_adjusted_jackpot_low31_r":obs,
      "year_stratified_p_exploratory":p,
      "association":associations,
      "years":{str(y):{"draws":len(v),"jackpot_winning_draws":sum(r["jackpot_won"] for r in v)}
               for y,v in sorted(groups.items())}}
# Predefined diagnostic: relative 4-match/3-match payout concentration for birthdate-range groups.
def group_label(n):
    return "0-2" if n<=2 else ("3" if n==3 else "4-6")
by_low={}
for key in ("0-2","3","4-6"):
    g=[r for r in usable if group_label(r["low31"])==key]
    by_low[key]={"draws":len(g),"jackpot_won":sum(r["jackpot_won"] for r in g),
                 "avg_normalized4":average(g,"ratio4_vs_uniform"),
                 "avg_normalized5":average(g,"ratio5_vs_uniform"),
                 "avg_sales_equivalent":average(g,"sales_equivalent_from_n3")}
kpis["by_low31_groups"]=by_low
kpis["ratio4_by_year"]={str(year):{"draws":len(group),
    "corr_low31_vs_normalized4":corr([r["low31"] for r in group],
                                      [r["ratio4_vs_uniform"] for r in group]),
    "mean_normalized4":average(group,"ratio4_vs_uniform")}
    for year,group in sorted(groups.items())}
# Year-stratified permutation of the association (exploratory; same year, fixed group sizes).
obs4=year_adjusted_corr(usable,"low31","ratio4_vs_uniform")
ge4=0
rng4=random.Random(20261104)
for _ in range(B):
    shuffled=[]
    for year,items in groups.items():
        perm=[r["ratio4_vs_uniform"] for r in items];rng4.shuffle(perm)
        shuffled.extend([{**r,"ratio4_vs_uniform":v} for r,v in zip(items,perm)])
    z=year_adjusted_corr(shuffled,"low31","ratio4_vs_uniform")
    if obs4 is not None and z is not None and abs(z)>=abs(obs4): ge4+=1
kpis["year_adjusted_ratio4_low31_r"]=obs4
kpis["year_stratified_ratio4_p_exploratory"]=(ge4+1)/(B+1) if obs4 is not None else None

# Pre-draw jackpot proxy: previous draw's displayed jackpot pool; after any Jackpot1
# win the next cycle is reset to the guaranteed 30 billion VND minimum.
by_id={int(r["id"]):r for r in usable}
for r in usable:
    p=by_id.get(int(r["id"])-1)
    if p and p["date"]<r["date"]:
        r["pre_draw_jackpot_proxy_vnd"] = 30_000_000_000 if p["jackpot_won"] else p["jackpot1_amount_vnd"]
    else: r["pre_draw_jackpot_proxy_vnd"]=None
pre=[r for r in usable if r["pre_draw_jackpot_proxy_vnd"] is not None]
kpis["predraw_jackpot_proxy"]={
    "n":len(pre),
    "correlation_with_sales_equivalent":year_adjusted_corr(pre,"pre_draw_jackpot_proxy_vnd","sales_equivalent_from_n3"),
    "correlation_with_normalized4":year_adjusted_corr(pre,"pre_draw_jackpot_proxy_vnd","ratio4_vs_uniform"),
    "correlation_with_normalized5":year_adjusted_corr(pre,"pre_draw_jackpot_proxy_vnd","ratio5_vs_uniform"),
    "correlation_with_jackpot_winner":year_adjusted_corr(pre,"pre_draw_jackpot_proxy_vnd","jackpot_won")
}
pool_groups={"<=60b":[],"60-150b":[],">150b":[]}
for r in pre:
    p=r["pre_draw_jackpot_proxy_vnd"]
    group="<=60b" if p<=60_000_000_000 else ("60-150b" if p<=150_000_000_000 else ">150b")
    pool_groups[group].append(r)
kpis["predraw_jackpot_groups"]={
    key:{"n":len(rows),"jackpot_owner_draws":sum(r["jackpot_won"] for r in rows),
         "mean_sales_equivalent":average(rows,"sales_equivalent_from_n3"),
         "mean_normalized4":average(rows,"ratio4_vs_uniform"),
         "low31_ratio4_correlation":corr([r["low31"] for r in rows],
                                          [r["ratio4_vs_uniform"] for r in rows])}
    for key,rows in pool_groups.items()}

# Jackpot 1 owner-event sequence from all validated draws (unlike 41-event press list).
# Prize source 'amount' is treated as a per-winning-ticket value when owner count > 0;
# total_pool is provisional until provider-specific units are independently confirmed.
events=sorted([r for r in usable if r["jackpot1_count"]>0],key=lambda x:int(x["id"]))
transitions=[]
for prev,cur in zip(events,events[1:]):
    transitions.append({"gap_draws":int(cur["id"])-int(prev["id"]),
      "year":cur["year"],"later_pool":cur["jackpot1_amount_vnd"]*cur["jackpot1_count"],
      "later_low31":cur["low31"],"later_sum":cur["sum"],"later_owners":cur["jackpot1_count"],
      "prev_id":prev["id"],"later_id":cur["id"]})
kpis["jackpot_event_sequence"]={
  "events":len(events),"transitions":len(transitions),
  "multi_owner_events":sum(e["jackpot1_count"]>=2 for e in events),
  "max_owners":max(e["jackpot1_count"] for e in events) if events else None,
  "mean_event_gap":average(transitions,"gap_draws"),
  "corr_gap_with_pool":corr([e["gap_draws"] for e in transitions],[e["later_pool"] for e in transitions]),
  "corr_pool_with_low31":corr([e["later_pool"] for e in transitions],[e["later_low31"] for e in transitions]),
  "year_adj_pool_with_low31":year_adjusted_corr(transitions,"later_pool","later_low31"),
  "corr_pool_with_sum":corr([e["later_pool"] for e in transitions],[e["later_sum"] for e in transitions]),
  "multiholder_low31_mean":average([e for e in events if e["jackpot1_count"]>=2],"low31"),
  "singleholder_low31_mean":average([e for e in events if e["jackpot1_count"]==1],"low31"),
  "event_ids_multi_owner":[e["id"] for e in events if e["jackpot1_count"]>=2]
}

# Uniform-choice ownership benchmark using sales-equivalent (not actual sales).
# A fair drawing of balls does not imply players choose combinations uniformly.
for r in usable:
    r["uniform_owner_expectation_proxy"]=-math.expm1(-r["sales_equivalent_from_n3"]/D)
kpis["uniform_owner_proxy"]={
  "expected_jackpot_winning_draws":sum(r["uniform_owner_expectation_proxy"] for r in usable),
  "actual_jackpot_winning_draws":sum(r["jackpot_won"] for r in usable),
  "by_low31":{key:{
    "n":len(g),
    "actual":sum(r["jackpot_won"] for r in g),
    "expected_uniform":sum(r["uniform_owner_expectation_proxy"] for r in g)}
    for key in ("0-2","3","4-6")
    for g in [[r for r in usable if group_label(r["low31"])==key]]}
}

with (OUT/"matched_draw_prizes.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=list(usable[0]));w.writeheader();w.writerows(usable)
(OUT/"summary.json").write_text(json.dumps(kpis,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
lines=[
"# Champion-X: full prize-tier player-choice audit — automatically generated",
"",
f"Matched valid draws: **{len(usable)}** of {len(details)} prize rows. Jackpot 1 winning draws: **{kpis['jackpot1_winning_draws']}**.",
f"Rejected records: `{json.dumps(dict(reasons),ensure_ascii=False)}`.",
"",
"**Data quality:** Missing / zero prize-tier records are excluded rather than treated as no sales.",
"Source data are third-party scraped and not officially audited. Align draw date and six main balls before scoring.",
"",
"## Baseline and descriptive results",
f"- Uniform 3/6 probability per ticket: `{p3:.8f}`.",
f"- Theoretical 4/6 count divided by 3/6 count: `{p4/p3:.8f}`.",
f"- Mean observed-normalized 4/6-to-3/6 ratio: `{kpis['mean_ratio4']:.4f}`.",
f"- Mean observed-normalized 5/6-to-3/6 ratio: `{kpis['mean_ratio5']:.4f}`.",
f"- Year-adjusted correlation of Jackpot 1 winning indicator with number of winning balls <=31: `{obs}`.",
f"- Year-only permutation p (not sales-adjusted, exploratory): `{p}`.",
"",
"## Correlations with prior draw-number descriptions",
"| outcome | feature | raw r | year-adjusted r |",
"|---|---|---:|---:|"
]
for m in metrics:
    for f in features:
        x=associations[m][f]
        lines.append(f"| {m} | {f} | {x['pearson'] if x['pearson'] is not None else 'NA'} | {x['year_adjusted'] if x['year_adjusted'] is not None else 'NA'} |")
lines+=["","## Interpretation / hard limits",
"- This is **not a ball forecasting test**. A prize-winning count is a *post-draw* statistic reflecting ticket popularity and sales.",
"- n3/p3 is only a sales-equivalent proxy assuming uniform ticket choices; actual choices are nonuniform.",
"- Normalized prize-tier ratios can suggest player number/combination preferences but do not reveal the exact popularity of a six-number combination.",
"- Simple associations are vulnerable to different sales volumes, changes in payout rules, digit preferences, repeated game entries, multiple comparisons and selective historical inspection.",
"- Do not promote X0, R19 or any new selection parameter from this analysis. For reliable claims obtain ticket sales and official prize ledger; perform prospectively pre-registered validation.",
""]
(OUT/"FULL_PRIZE_TIER_AUDIT.md").write_text("\n".join(lines),encoding="utf-8")
print("RESULT_JSON="+json.dumps({k:v for k,v in kpis.items() if k!="association"},ensure_ascii=False))
print("RESULT_CORRELATIONS="+json.dumps(associations,ensure_ascii=False))
