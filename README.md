# DF-162 OPS-Onboarding-Workflow [CRUX-MK]

**Status:** SKELETON-CONDITIONAL (Welle-51 W51-B Skeleton-Wave-2)
**Domain:** OPS (Operational HR-Onboarding)
**Welle:** 25

## Mission

Onboarding-Step-Completion-Tracking. Tracking:
- Pending-Onboardings
- Median-Completion-Time-Days
- Step-Completion-Rate-Pct
- Stale-Onboardings-30d

**NIEMALS Onboarding-Steps automatisch abschliessen.**

## Usage

```bash
cd ~/Projects/dark-factories/df-162
python df-162-engine.py        # Mock-Mode default
pytest tests/                   # Existing tests
```

## Output

- Reports: `reports/df-162-{date}.json`
- STOP-Flag: `/tmp/df-162.stop`

[CRUX-MK]
