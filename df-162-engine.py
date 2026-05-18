
# K16: Concurrent-Spawn-Mutex (fcntl-based, Trinity-CONSERVATIVE 2026-05-17)
def k16_lock_or_exit(df_name: str):
    """Acquire exclusive lock or exit(3). Prevents concurrent DF runs."""
    import fcntl, os, sys
    lock_path = f"/tmp/df-trinity-{df_name}.lock"
    fd = os.open(lock_path, os.O_CREAT | os.O_WRONLY)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return fd
    except BlockingIOError:
        sys.exit(3)


# K13: External-Anchor-Mock-RFC3161 (Trinity-CONSERVATIVE 2026-05-17)
def k13_anchor(payload_hash: str) -> dict:
    """Mock RFC3161-style timestamp anchor."""
    from datetime import datetime, timezone
    return {
        "anchor_type": "rfc3161-mock",
        "iso_ts": datetime.now(timezone.utc).isoformat(),
        "payload_hash": payload_hash,
    }


# K12: HMAC-SHA256-Provenance (Trinity-CONSERVATIVE 2026-05-17)
def k12_provenance(payload: bytes, key: bytes = b"df-trinity-conservative-v1") -> dict:
    """Returns payload_hash + HMAC-SHA256 signature."""
    import hashlib, hmac
    return {
        "payload_hash": hashlib.sha256(payload).hexdigest(),
        "hmac_sha256": hmac.new(key, payload, hashlib.sha256).hexdigest(),
    }

"""DF-162 OPS-Onboarding-Workflow tracker engine."""

import re
import os
import json
import sys
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from datetime import datetime, timezone


DF_DIR = Path(__file__).parent
LOCK_DIR = Path("/tmp/df-162.lock")
DF_ID = "162"
DECISION_KEYWORDS_REGEX = re.compile(
    r"\b(entscheid[a-z]*|empfehl(?:e|en|t|st)|sollt(?:e|en|est)|recommend[a-z]*|decid[a-z]*|advis[a-z]*|propos[a-z]*)\b",
    re.IGNORECASE,
)


@dataclass
class TrackerOutput:
    welle: str = "25"
    df: str = "DF-162"
    iso_timestamp: str = ""
    source: str = "mock"
    active_onboardings: int = 0
    average_onboarding_days: float = 0
    completion_rate_pct: float = 0
    drop_off_phase: str = ""
    top_blockers: list = field(default_factory=list)


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _file_stable(path, min_age_sec=300) -> bool:
    p = Path(path)
    if not p.exists():
        return False
    try:
        return time.time() - p.stat().st_mtime >= min_age_sec
    except OSError:
        return False


def acquire_lock_with_identity() -> bool:
    stale_after_sec = 6 * 60 * 60
    now = time.time()

    try:
        LOCK_DIR.mkdir(mode=0o700)
    except FileExistsError:
        try:
            age = now - LOCK_DIR.stat().st_mtime
        except OSError:
            return False

        if age < stale_after_sec:
            return False

        try:
            for child in LOCK_DIR.iterdir():
                if child.is_file() or child.is_symlink():
                    child.unlink()
                elif child.is_dir():
                    child.rmdir()
            LOCK_DIR.rmdir()
            LOCK_DIR.mkdir(mode=0o700)
        except OSError:
            return False
    except OSError:
        return False

    identity = {
        "df_id": DF_ID,
        "pid": os.getpid(),
        "created_at": iso_now(),
        "cwd": str(Path.cwd()),
        "argv": sys.argv,
    }

    try:
        (LOCK_DIR / "identity.json").write_text(
            json.dumps(identity, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except OSError:
        release_lock()
        return False

    return True


def release_lock() -> None:
    try:
        if not LOCK_DIR.exists():
            return
        for child in LOCK_DIR.iterdir():
            if child.is_file() or child.is_symlink():
                child.unlink()
            elif child.is_dir():
                child.rmdir()
        LOCK_DIR.rmdir()
    except OSError:
        pass


def k17_pre_action_verification(anchors) -> dict:
    missing = []
    for anchor in anchors or []:
        if not Path(anchor).exists():
            missing.append(str(anchor))

    return {
        "ok": not missing,
        "missing_anchors": missing,
        "env_tag": "real" if _is_real_api_enabled() else "mock",
    }


def _is_real_api_enabled() -> bool:
    value = os.getenv("DF_162_REAL_API_ENABLED", "false").strip().lower()
    return value in {"1", "true", "yes", "y", "on"}


def scan_output_for_decision_keywords(text) -> list:
    if text is None:
        return []
    return sorted({m.group(0) for m in DECISION_KEYWORDS_REGEX.finditer(str(text))})


def assert_no_decision_keywords(output) -> None:
    hits = scan_output_for_decision_keywords(output)
    if hits:
        raise ValueError("Q_0/K_0 blocked decision keywords: " + ", ".join(hits))


def collect_tracker_output() -> TrackerOutput:
    source = "real" if _is_real_api_enabled() else "mock"

    if source == "real":
        data_path = Path(os.getenv("DF_162_REAL_API_JSON", ""))
        if data_path and data_path.exists() and _file_stable(data_path, 1):
            raw = json.loads(data_path.read_text(encoding="utf-8"))
            output = TrackerOutput(
                iso_timestamp=iso_now(),
                source="real",
                active_onboardings=int(raw.get("active_onboardings", 0)),
                average_onboarding_days=float(raw.get("average_onboarding_days", 0)),
                completion_rate_pct=float(raw.get("completion_rate_pct", 0)),
                drop_off_phase=str(raw.get("drop_off_phase", "")),
                top_blockers=list(raw.get("top_blockers", [])),
            )
            assert_no_decision_keywords(json.dumps(asdict(output), ensure_ascii=False))
            return output

    output = TrackerOutput(
        iso_timestamp=iso_now(),
        source="mock",
        active_onboardings=14,
        average_onboarding_days=18.5,
        completion_rate_pct=82.0,
        drop_off_phase="equipment_setup",
        top_blockers=["account_access", "device_delivery", "manager_intro"],
    )
    assert_no_decision_keywords(json.dumps(asdict(output), ensure_ascii=False))
    return output


def main() -> int:
    if not acquire_lock_with_identity():
        return 3

    try:
        pav = k17_pre_action_verification([DF_DIR])
        if not pav.get("ok"):
            return 3

        output = collect_tracker_output()
        payload = {
            "k17_pre_action_verification": pav,
            "tracker_output": asdict(output),
        }

        text = json.dumps(payload, ensure_ascii=False, indent=2)
        assert_no_decision_keywords(text)

        reports_dir = DF_DIR / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)

        date_tag = datetime.now(timezone.utc).date().isoformat()
        report_path = reports_dir / f"df-162-{date_tag}.json"
        report_path.write_text(text + "\n", encoding="utf-8")
        return 0
    except Exception as exc:
        sys.stderr.write(f"DF-162 failed: {exc}\n")
        return 3
    finally:
        release_lock()


if __name__ == "__main__":
    raise SystemExit(main())