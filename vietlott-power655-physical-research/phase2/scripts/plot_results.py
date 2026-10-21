"""Standalone scientific figure of visibility intervals; no inferred machine timer."""
import csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from build_results import ROOT
def main():
    target=ROOT/'charts'/'visible_cadence.png'
    if target.exists():raise SystemExit('Refuse overwrite')
    with (ROOT/'evidence'/'visible_cadence_intervals.csv').open(encoding='utf-8',newline='') as f:rows=list(csv.DictReader(f))
    fig,ax=plt.subplots(figsize=(10,5.5),layout='constrained')
    for j,draw in enumerate(['01372','01373','01374','01375','01376']):
        g=[r for r in rows if r['draw_id']==draw];x=[int(r['interval_index'])+(j-2)*.055 for r in g]
        lo=[float(r['duration_lower_seconds']) for r in g];hi=[float(r['duration_upper_seconds']) for r in g];mid=[(a+b)/2 for a,b in zip(lo,hi)]
        ax.errorbar(x,mid,yerr=[[m-a for m,a in zip(mid,lo)],[b-m for m,b in zip(mid,hi)]],fmt='o-',lw=1,markersize=4,capsize=2,label='#'+draw)
    ax.axvline(5.5,color='#888888',ls='--',lw=.8);ax.set_xticks(range(1,7),['1→2','2→3','3→4','4→5','5→6','6→special'])
    ax.set_ylabel('Visible downstream inter-entry interval (s)');ax.set_xlabel('Within-draw interval; five draws are the analysis units')
    ax.set_title('Broadcast transport cadence — visibility proxies only\nBounds show PTS localization, not confidence intervals or physical accuracy',fontsize=12)
    ax.grid(axis='y',alpha=.2);ax.legend(ncol=5,loc='lower center');fig.savefig(target,dpi=180);plt.close(fig)
    print(target)
if __name__=='__main__':main()
