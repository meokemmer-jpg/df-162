import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
# [CRUX-MK]
import importlib

m162 = importlib.import_module("162")
build_onboarding_report = m162.build_onboarding_report


def test_build_onboarding_report_tracks_core_metrics_without_auto_completing_steps():
    onboardings = [
        {
            "employee_id": "E-001",
            "created_at": "2026-01-01",
            "completed_at": "2026-01-06",
            "steps": [
                {"name": "docs", "completed": True, "completed_at": "2026-01-02"},
                {"name": "equipment", "completed": True, "completed_at": "2026-01-04"},
                {"name": "orientation", "completed": True, "completed_at": "2026-01-06"},
            ],
        },
        {
            "employee_id": "E-002",
            "created_at": "2026-01-10",
            "completed_at": "2026-01-18",
            "steps": [
                {"name": "docs", "completed": True, "completed_at": "2026-01-12"},
                {"name": "equipment", "completed": True, "completed_at": "2026-01-15"},
                {"name": "orientation", "completed": True, "completed_at": "2026-01-18"},
            ],
        },
        {
            "employee_id": "E-003",
            "created_at": "2026-01-01",
            "steps": [
                {"name": "docs", "completed": True, "completed_at": "2026-01-03"},
                {"name": "equipment", "completed": False, "completed_at": None},
                {"name": "orientation", "completed": False, "completed_at": None},
            ],
        },
    ]

    report = build_onboarding_report(onboardings, as_of="2026-02-15")

    assert report == {
        "pending_onboardings": 1,
        "median_completion_time_days": 6.5,
        "step_completion_rate_pct": 77.78,
        "stale_onboardings_30d": 1,
    }

    assert onboardings[2]["steps"][1]["completed"] is False
    assert onboardings[2]["steps"][2]["completed"] is False
