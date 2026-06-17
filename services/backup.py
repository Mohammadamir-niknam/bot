"""Daily backup archive utilities."""
from __future__ import annotations
import tarfile
from datetime import datetime, UTC
from pathlib import Path

class BackupService:
    def __init__(self, backup_dir: Path) -> None:
        self.backup_dir = backup_dir
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    def create_archive(self, *paths: Path) -> Path:
        target = self.backup_dir / f"backup-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}.tar.gz"
        with tarfile.open(target, "w:gz") as archive:
            for path in paths:
                if path.exists():
                    archive.add(path, arcname=path.name)
        return target
