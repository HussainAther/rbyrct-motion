import numpy as np
from pathlib import Path
from rbyrct_common import target_centered_candidates, ray_metrics, TARGET_CENTER_MM, save_json
def main():
    rows=[r for r in target_centered_candidates() if r["hit"]][:32]
    amps=[0,0.5,1,2,4]; out=[]
    for a in amps:
        ts=np.linspace(0,2*np.pi,100,endpoint=False)
        vals=[]
        for t in ts:
            c=TARGET_CENTER_MM+np.array([0.3*a*np.sin(t),a*np.sin(t),0.2*a*np.cos(t)])
            vals.append(np.mean([ray_metrics(r["source"],r["detector"],center=c)["hit"] for r in rows]))
        out.append({"motion_amplitude_mm":a,"mean_hit_fraction":float(np.mean(vals)),"worst_hit_fraction":float(np.min(vals))})
    save_json(Path("outputs")/"motion_sweep.json",out); print(out)
if __name__=="__main__": main()
