from __future__ import annotations
import math
import numpy as np

TARGET_CENTER_MM = np.array([12.0, 0.0, 5.0], dtype=float)
TARGET_DIAMETER_MM = 2.0
SOURCE_Y_MM = -110.0
DETECTOR_Y_MM = 110.0

def unit(v):
    v = np.asarray(v, dtype=float)
    n = np.linalg.norm(v)
    if n == 0:
        raise ValueError("zero vector")
    return v / n

def ray_metrics(source, detector, center=TARGET_CENTER_MM, radius=TARGET_DIAMETER_MM/2):
    s=np.asarray(source,float); d=np.asarray(detector,float); c=np.asarray(center,float)
    v=d-s
    vv=float(v@v)
    t=float(np.clip(-((s-c)@v)/vv,0,1))
    p=s+t*v
    closest=float(np.linalg.norm(p-c))
    a=vv; b=2*float((s-c)@v); cc=float((s-c)@(s-c)-radius*radius)
    disc=b*b-4*a*cc
    path=0.0; hit=False
    if disc>=0:
        q=math.sqrt(max(0.0,disc))
        r1=(-b-q)/(2*a); r2=(-b+q)/(2*a)
        lo=max(0.0,min(r1,r2)); hi=min(1.0,max(r1,r2))
        if hi>=lo:
            hit=True; path=float(np.linalg.norm((s+hi*v)-(s+lo*v)))
    direction=unit(v)
    az=float(np.degrees(np.arctan2(direction[0],direction[1])))
    el=float(np.degrees(np.arctan2(direction[2],np.hypot(direction[0],direction[1]))))
    return {"hit":hit,"closest_mm":closest,"path_mm":path,"azimuth_deg":az,"elevation_deg":el}

def target_centered_candidates(nx=7,nz=7, offsets=(-2,-1,0,1,2), target=TARGET_CENTER_MM):
    xs=np.linspace(-42,42,nx); zs=np.linspace(-42,42,nz)
    out=[]; rid=0
    for sx in xs:
        for sz in zs:
            s=np.array([sx,SOURCE_Y_MM,sz],float)
            t=(DETECTOR_Y_MM-s[1])/(target[1]-s[1])
            ideal=s+t*(target-s)
            for dx in offsets:
                for dz in offsets:
                    d=ideal+np.array([dx,0,dz],float)
                    if abs(d[0])>50 or abs(d[2])>50:
                        continue
                    m=ray_metrics(s,d,center=target)
                    out.append({"ray_id":rid,"source":s.tolist(),"detector":d.tolist(),**m})
                    rid+=1
    return out

def angular_sep(a,b):
    a=unit(np.asarray(a)); b=unit(np.asarray(b))
    return float(np.degrees(np.arccos(np.clip(a@b,-1,1))))

def ray_dir(row):
    return unit(np.asarray(row["detector"])-np.asarray(row["source"]))

def save_json(path,obj):
    from pathlib import Path
    import json
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,indent=2)+"\n",encoding="utf-8")
