#!/usr/bin/env python3
"""POWER 6/55 physical-draw pilot: null/calibration ONLY; draw-order data absent.
Tests unconditional six-number inclusion and special-ball marginal frequency.
Run with Python 3.11. No Frozen modifications, no predictive algorithm.
"""
import csv,hashlib,json,math,random,urllib.request
from collections import Counter
from pathlib import Path

HERE=Path(__file__).resolve().parent
OUT=HERE/"physical_draw_pilot_outputs"
OUT.mkdir(exist_ok=True)
URL="https://raw.githubusercontent.com/vietvudanh/vietlott-data/main/data/power655.jsonl"
def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Champion-X-Physical-Audit/1.0"}),timeout=60) as r:return r.read()
raw=fetch(URL)
data=[json.loads(x) for x in raw.decode().splitlines() if x.strip()]
records=[];bad=[];seen=set()
for r in data:
    try:
        id=int(r["id"])
        main=list(map(int,r["result"][:6]));bonus=int(r["result"][6])
        assert id not in seen and len(main)==6 and len(set(main))==6
        assert all(1<=n<=55 for n in main) and 1<=bonus<=55 and bonus not in main
        records.append((id,r["date"],tuple(sorted(main)),bonus));seen.add(id)
    except (KeyError,IndexError,TypeError,ValueError,AssertionError) as e:bad.append({"id":r.get("id"),"error":str(e)})
records.sort(key=lambda x:x[0])
assert len(records)>=1000 and len(bad)<=3
# Explicit quarantine of malformed source records; report them in output.
N=len(records);six=Counter(x for r in records for x in r[2]);special=Counter(r[3] for r in records)
expected_main=N*6/55;expected_special=N/55
# fixed multinomial/combinatorial complete-basket null; adjust per-number variance
v_main=N*(6/55)*(49/55);v_special=N*(1/55)*(54/55)
def chi(c,expected):
    return sum((c.get(n,0)-expected)**2/expected for n in range(1,56))
def maxz(c,expected,var):
    return max(abs(c.get(n,0)-expected)/math.sqrt(var) for n in range(1,56))
obs_chi_main=chi(six,expected_main);obs_chi_special=chi(special,expected_special)
obs_mz_main=maxz(six,expected_main,v_main);obs_mz_special=maxz(special,expected_special,v_special)
def overlap(a,b):return len(set(a)&set(b))
adjacent=[overlap(records[i-1][2],records[i][2]) for i in range(1,N) if records[i][0]==records[i-1][0]+1]
overlap_sum=sum(adjacent)
expected_overlap=len(adjacent)*36/55
# Independent hypergeometric sets of six overlap, expected 36/55
seed=20261103;rng=random.Random(seed)
B=500;hi_main=hi_special=hi_mz_main=hi_mz_special=hi_overlap=lo_overlap=0
for j in range(B):
    mains=[0]*56;bonuses=[0]*56;osum=0;prev=None
    for i in range(N):
        seven=rng.sample(range(1,56),7)
        cur=set(seven[:6])
        for x in cur:mains[x]+=1
        bonuses[seven[6]]+=1
        if prev is not None and records[i][0]==records[i-1][0]+1:osum+=len(prev&cur)
        prev=cur
    cm=sum((mains[x]-expected_main)**2/expected_main for x in range(1,56))
    cb=sum((bonuses[x]-expected_special)**2/expected_special for x in range(1,56))
    zm=max(abs(mains[x]-expected_main)/math.sqrt(v_main) for x in range(1,56))
    zb=max(abs(bonuses[x]-expected_special)/math.sqrt(v_special) for x in range(1,56))
    hi_main+=cm>=obs_chi_main
    hi_special+=cb>=obs_chi_special
    hi_mz_main+=zm>=obs_mz_main
    hi_mz_special+=zb>=obs_mz_special
    hi_overlap+=osum>=overlap_sum
    lo_overlap+=osum<=overlap_sum
p=lambda x:(x+1)/(B+1)
out={
  "scope":"public 6-number result plus seventh special; NO draw-order or ball-set identifiers",
  "source_sha256":hashlib.sha256(raw).hexdigest(),
  "raw_count":len(data),"valid_count":N,"first_id":records[0][0],"last_id":records[-1][0],
  "data_quality":{"invalid_records":bad,"id_gaps":sum((b[0]-a[0]>1) for a,b in zip(records,records[1:]))},
  "null":"independent uniform sampling without replacement: six unordered mains and special as 7th",
  "monte_carlo":{"seed":seed,"replicates":B},
  "main":{"expected_count_per_number":expected_main,"chi_square":obs_chi_main,
          "mc_upper_tail_p":p(hi_main),"max_abs_z":obs_mz_main,"mc_fwer_p":p(hi_mz_main)},
  "special":{"expected_count_per_number":expected_special,"chi_square":obs_chi_special,
          "mc_upper_tail_p":p(hi_special),"max_abs_z":obs_mz_special,"mc_fwer_p":p(hi_mz_special)},
  "serial_main_overlap":{"observed_mean":overlap_sum/len(adjacent),"num_adjacent_pairs":len(adjacent),
       "expected_mean":36/55,
       "mc_two_sided_p":min(1,2*min(p(hi_overlap),p(lo_overlap)))},
  "critical_limitations":[
    "Sorting historical winning labels in output does NOT reconstruct physical extraction order.",
    "Physical machine, ball-case ID, measured individual ball mass/diameter and extraction times remain unknown.",
    "All tests exploratory and do not establish a physical cause. MC uncertainty with 500 replicates is substantial.",
    "This raw public historical window has previously been reused for algorithm research and is not untouched OOS.",
    "Even a significant departure needs device-stratified prospective confirmation and predicted inclusion advantage before use."
  ]}
(OUT/"summary.json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n")
with (OUT/"number_counts.csv").open("w",newline="") as f:
    w=csv.writer(f);w.writerow(["number","main_count","bonus_count","expected_main","expected_bonus"])
    for n in range(1,56):w.writerow([n,six[n],special[n],expected_main,expected_special])
print("RESULT_JSON="+json.dumps(out,ensure_ascii=False))
