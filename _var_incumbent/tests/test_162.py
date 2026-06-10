import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
# [CRUX-MK]
import importlib

m162 = importlib.import_module("162")
calculate_onboarding_metrics = m162.calculate_onboarding_metrics
OnboardingMetrics = m162.OnboardingMetrics


def test_calculate_onboarding_metrics_tracks_pending_completed_and_stale_without_auto_completion():
    onboardings = [
        {
            "employee_id": "emp-1",
            "created_at": "2026-01-01",
            "last_activity_at": "2026-01-15",
            "steps": [
                {"name": "contract", "completed_at": "2026-01-03"},
                {"name": "device", "completed_at": "2026-01-05"},
            ],
        },
        {
            "employee_id": "emp-2",
            "created_at": "2026-01-10",
            "last_activity_at": "2026-01-20",
            "steps": [
                {"name": "contract", "completed_at": "2026-01-12"},
                {"name": "device", "completed_at": None},
            ],
        },
        {
            "employee_id": "emp-3",
            "created_at": "2026-01-20",
            "last_activity_at": "2026-03-15",
            "steps": [
                {"name": "contract", "completed_at": "2026-01-25"},
                {"name": "device", "completed_at": "2026-01-29"},
            ],
        },
        {
            "employee_id": "emp-4",
            "created_at": "2026-02-01",
            "last_activity_at": "2026-02-05",
            "steps": [
                {"name": "contract", "completed_at": None},
                {"name": "device", "completed_at": None},
            ],
        },
    ]

    result = calculate_onboarding_metrics(onboardings, reference_date="2026-03-20")

    assert isinstance(result, OnboardingMetrics)
    assert result.pending_onboardings == 2
    assert result.median_completion_time_days == 6.5
    assert result.step_completion_rate_pct == 50.0
    assert result.stale_onboardings_30d == 2

    # Mission constraint: stale or partial onboardings stay pending until steps are explicitly completed.
    assert onboardings[1]["steps"][1]["completed_at"] is None
    assert onboardings[3]["steps"][0]["completed_at"] is None
    assert onboardings[3]["steps"][1]["completed_at"] is None

