from __future__ import annotations

from datetime import date, datetime
from statistics import median
from typing import Iterable, Mapping, Any


def _to_date(value: Any) -> date | None:
    if value is None:
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, str):
        return date.fromisoformat(value)
    raise TypeError(f"Unsupported date value: {value!r}")


def _is_step_completed(step: Mapping[str, Any]) -> bool:
    return bool(step.get("completed", False))


def _onboarding_is_completed(onboarding: Mapping[str, Any]) -> bool:
    steps = onboarding.get("steps", [])
    return bool(steps) and all(_is_step_completed(step) for step in steps)


def pending_onboardings(onboardings: Iterable[Mapping[str, Any]]) -> int:
    return sum(1 for onboarding in onboardings if not _onboarding_is_completed(onboarding))


def median_completion_time_days(onboardings: Iterable[Mapping[str, Any]]) -> float | None:
    durations = []

    for onboarding in onboardings:
        if not _onboarding_is_completed(onboarding):
            continue

        created_at = _to_date(onboarding.get("created_at"))
        if created_at is None:
            raise ValueError("Completed onboarding is missing created_at")

        completed_at = _to_date(onboarding.get("completed_at"))
        if completed_at is None:
            step_dates = [
                _to_date(step.get("completed_at"))
                for step in onboarding.get("steps", [])
                if _is_step_completed(step)
            ]
            if len(step_dates) != len(onboarding.get("steps", [])) or any(d is None for d in step_dates):
                raise ValueError("Completed onboarding requires completed_at or completed_at on every completed step")
            completed_at = max(step_dates)

        durations.append((completed_at - created_at).days)

    if not durations:
        return None
    return float(median(durations))


def step_completion_rate_pct(onboardings: Iterable[Mapping[str, Any]]) -> float:
    total_steps = 0
    completed_steps = 0

    for onboarding in onboardings:
        steps = onboarding.get("steps", [])
        total_steps += len(steps)
        completed_steps += sum(1 for step in steps if _is_step_completed(step))

    if total_steps == 0:
        return 0.0
    return round((completed_steps / total_steps) * 100.0, 2)


def stale_onboardings_30d(onboardings: Iterable[Mapping[str, Any]], as_of: Any = None) -> int:
    as_of_date = _to_date(as_of) or date.today()
    stale = 0

    for onboarding in onboardings:
        if _onboarding_is_completed(onboarding):
            continue

        created_at = _to_date(onboarding.get("created_at"))
        if created_at is None:
            raise ValueError("Pending onboarding is missing created_at")

        if (as_of_date - created_at).days >= 30:
            stale += 1

    return stale


def build_onboarding_report(onboardings: Iterable[Mapping[str, Any]], as_of: Any = None) -> dict[str, Any]:
    onboardings = list(onboardings)
    return {
        "pending_onboardings": pending_onboardings(onboardings),
        "median_completion_time_days": median_completion_time_days(onboardings),
        "step_completion_rate_pct": step_completion_rate_pct(onboardings),
        "stale_onboardings_30d": stale_onboardings_30d(onboardings, as_of=as_of),
    }
# [CRUX-MK]
