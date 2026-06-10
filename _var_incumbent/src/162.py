from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from statistics import median
from typing import Iterable, Optional


@dataclass(frozen=True)
class OnboardingMetrics:
    pending_onboardings: int
    median_completion_time_days: Optional[float]
    step_completion_rate_pct: float
    stale_onboardings_30d: int


def _to_date(value) -> date:
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, str):
        return date.fromisoformat(value)
    raise TypeError(f"Unsupported date value: {value!r}")


def _is_step_completed(step: dict) -> bool:
    return step.get("completed_at") is not None


def calculate_onboarding_metrics(
    onboardings: Iterable[dict],
    reference_date=None,
) -> OnboardingMetrics:
    ref = _to_date(reference_date) if reference_date is not None else date.today()

    pending_count = 0
    stale_count = 0
    completion_durations = []
    total_steps = 0
    completed_steps = 0

    for onboarding in onboardings:
        created_at = _to_date(onboarding["created_at"])
        last_activity_raw = onboarding.get("last_activity_at", created_at)
        last_activity_at = _to_date(last_activity_raw)
        steps = list(onboarding.get("steps", []))

        total_steps += len(steps)
        completed_steps += sum(1 for step in steps if _is_step_completed(step))

        all_steps_completed = bool(steps) and all(_is_step_completed(step) for step in steps)

        if all_steps_completed:
            completed_dates = [_to_date(step["completed_at"]) for step in steps]
            finished_at = max(completed_dates)
            completion_durations.append((finished_at - created_at).days)
        else:
            pending_count += 1
            if (ref - last_activity_at).days >= 30:
                stale_count += 1

    completion_rate = 0.0
    if total_steps:
        completion_rate = round((completed_steps / total_steps) * 100, 2)

    median_days = None
    if completion_durations:
        median_days = float(median(completion_durations))

    return OnboardingMetrics(
        pending_onboardings=pending_count,
        median_completion_time_days=median_days,
        step_completion_rate_pct=completion_rate,
        stale_onboardings_30d=stale_count,
    )
# [CRUX-MK]
