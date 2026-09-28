from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path


def default_audit_log_path() -> str:
    """Always resolve to <repo>/outputs/? (safe when cwd is src/)."""
    repo_root = Path(__file__).resolve().parents[2]
    return str(repo_root / "outputs" / "audit_log.json")


class AuditLogPlugin:
    """Framework-agnostic audit logger (wire into ADK callbacks or your pipeline)."""

    def __init__(self):
        self.name = "audit_log"
        self.logs: list[dict] = []
        self._open: dict[str, float] = {}

    def record_input(self, *, user_id: str, text: str, request_id: str | None = None):
        """Store input + start timestamp keyed by request_id/user_id."""
        key = request_id or user_id
        self._open[key] = time.time()
        self.logs.append({
            "request_id": request_id,
            "user_id": user_id,
            "input": text,
            "timestamp": utc_now_iso()
        })

    def record_output(
        self,
        *,
        user_id: str,
        text: str,
        blocked: bool = False,
        layer: str | None = None,
        request_id: str | None = None,
    ):
        """Store output, layer decision, latency; append to self.logs."""
        key = request_id or user_id
        start_time = self._open.pop(key, time.time())
        latency = time.time() - start_time
        
        # Find the input log and update it with output details
        for log in reversed(self.logs):
            if log.get("request_id") == request_id and log.get("user_id") == user_id:
                log.update({
                    "output": text,
                    "blocked": blocked,
                    "layer": layer,
                    "latency": latency,
                    "completed_at": utc_now_iso()
                })
                break

    def export_json(self, filepath: str | None = None):
        """Write logs to disk (JSON array) under repo-root ``outputs/`` by default."""
        path = filepath or default_audit_log_path()
        out_path = Path(path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(self.logs, f, indent=2, ensure_ascii=False)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
