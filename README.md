# rbyrct-motion

## Research question

Stress-test targeting under respiratory-like translation and deformation surrogates.

## v0.1 scope

This is a runnable **baseline research scaffold**, not a clinical claim or validated scanner implementation.

Shared conventions:

- canonical geometry unit: millimeter;
- default target: 2 mm sphere at `[12, 0, 5] mm`;
- default evidence level: `E0` geometric/proxy unless explicitly stated otherwise;
- conceptual source/detector geometry must not be presented as validated hardware;
- saved outputs are machine-readable JSON.

## Run on Windows / RTX 4070 laptop

```powershell
cd C:\Users\shuss\Downloads\rbyrct\rbyrct-motion
python -m venv .venv
.venv\Scripts\activate
python -m pip install -e ".[dev]"
pytest -q
python scripts\run_baseline.py
```

The v0.1 baselines are intentionally lightweight and CPU-first. The RTX 4070 becomes useful when the candidate space, reconstruction, VICTRE processing, learned models, or Monte Carlo workload grows.

## Scientific caution

Proxy metrics are labeled as proxies. No repo should imply clinical validation, physical dose validation, or working electronically steerable hardware unless supported by separate evidence.
