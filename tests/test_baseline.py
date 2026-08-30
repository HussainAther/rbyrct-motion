import numpy as np
from rbyrct_common import ray_metrics, TARGET_CENTER_MM

def test_central_target_ray_hits():
    s=np.array([12.,-110.,5.])
    d=np.array([12.,110.,5.])
    m=ray_metrics(s,d)
    assert m["hit"]
    assert abs(m["path_mm"]-2.0)<1e-9
