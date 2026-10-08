#!/usr/bin/env python3
"""Power 6/55 v0.4.0 — sequential probability model, no portfolio optimization."""
import argparse, json, math
from pathlib import Path
P=6/55
WINDOWS=(0,30,60,120,365)
def load(path):
    rows=[json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
    last="";seen=set()
    for row in rows:
        a=row["result"][:6]
        if len(a)!=6 or len(set(a))!=6 or any(type(n)!=int or n<1 or n>55 for n in a):raise ValueError("Invalid draw")
        if row["date"]<last or row["id"] in seen:raise ValueError("Unsorted/duplicate")
        last=row["date"];seen.add(row["id"])
    return rows
def features(rows,t):
    result=[]
    for w in WINDOWS:
        sample=rows[max(0,t-w):t] if w else rows[:t]
        c=[0]*56
        for row in sample:
            for n in row["result"][:6]:c[n]+=1
        result.append([(c[n]+20*P)/(len(sample)+20) for n in range(1,56)])
    return [[result[j][i] for j in range(5)] for i in range(55)]
def predict(F,weights):
    raw=[sum(x*w for x,w in zip(row,weights)) for row in F]
    z=sum(raw)
    return [6*x/z for x in raw]
def metrics(probs,draw):
    actual=set(draw["result"][:6]);brier=logloss=0
    for i,q in enumerate(probs):
        y=int(i+1 in actual);q=max(1e-9,min(1-1e-9,q))
        brier+=(q-y)**2/55
        logloss+=-(y*math.log(q)+(1-y)*math.log(1-q))/55
    rank=sorted(range(1,56),key=lambda n:(-probs[n-1],n))
    return {"brier":brier,"logloss":logloss,"top6":len(set(rank[:6])&actual),
            "top18":len(set(rank[:18])&actual)}
def replay(rows,start,end,eta):
    weights=[.2]*5;records=[]
    for t in range(start,end):
        F=features(rows,t)
        forecast=predict(F,weights)
        # Forecast is constructed before the current draw is revealed.
        result=metrics(forecast,rows[t])
        uniform=metrics([P]*55,rows[t])
        losses=[metrics(predict(F,[int(i==j) for i in range(5)]),rows[t])["brier"] for j in range(5)]
        prior=weights[:]
        weights=[w*math.exp(-eta*loss) for w,loss in zip(weights,losses)]
        z=sum(weights);weights=[w/z for w in weights]
        records.append({"id":rows[t]["id"],"date":rows[t]["date"],"forecast_metrics":result,
                        "uniform_metrics":uniform,"weights_before":prior,"weights_after":weights})
    return records,weights
def summary(records,key):
    return {k:sum(r[key][k] for r in records)/len(records) for k in ("brier","logloss","top6","top18")}
def run(rows):
    training=[{"eta":eta,"metrics":summary(replay(rows,1000,1250,eta)[0],"forecast_metrics")}
              for eta in (1,5,20,50)]
    chosen=min(training,key=lambda x:x["metrics"]["brier"])["eta"]
    val,_=replay(rows,1250,1394,chosen)
    test,_=replay(rows,1394,1408,chosen)
    full,weights=replay(rows,1000,len(rows),chosen)
    probs=predict(features(rows,len(rows)),weights)
    ranking=sorted(range(1,56),key=lambda n:(-probs[n-1],n))
    return {"version":"0.4.0","eta":chosen,"training":training,
            "validation":{"model":summary(val,"forecast_metrics"),"uniform":summary(val,"uniform_metrics")},
            "holdout":{"model":summary(test,"forecast_metrics"),"uniform":summary(test,"uniform_metrics")},
            "holdout_replay":test,"final_weights":weights,
            "next_probabilities":{str(n):probs[n-1] for n in range(1,56)},
            "next_ranked_numbers":ranking}
if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--data",required=True);ap.add_argument("--output",default="results_v040.json")
    args=ap.parse_args();rows=load(args.data)
    if len(rows)!=1408:raise ValueError("v0.4.0 reproducibility split expects exactly 1408 draws through #01408")
    report=run(rows)
    Path(args.output).write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps({k:report[k] for k in ("version","eta","validation","holdout","final_weights")},indent=2))
