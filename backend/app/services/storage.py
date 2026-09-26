from pathlib import Path
from uuid import uuid4
from . import __name__
from ..config import get_settings

settings = get_settings()

class StorageService:
    def __init__(self):
        self.mode = settings.storage_mode
        if self.mode == "local":
            Path(settings.local_upload_dir).mkdir(parents=True, exist_ok=True)
        else:
            from supabase import create_client
            self.client = create_client(settings.supabase_url, settings.supabase_service_role_key)

    def upload(self, content: bytes, original_name: str, assignment_id: int, student_id: int):
        suffix = Path(original_name).suffix.lower()
        path = f"assignments/assignment_{assignment_id}/student_{student_id}/{uuid4().hex}{suffix}"
        if self.mode == "local":
            target = Path(settings.local_upload_dir) / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
            return path, None
        self.client.storage.from_(settings.supabase_bucket).upload(path, content, {"content-type": "application/octet-stream", "upsert": "false"})
        return path, None

    def download(self, path: str):
        if self.mode == "local":
            target = Path(settings.local_upload_dir) / path
            if not target.exists(): raise FileNotFoundError(path)
            return target.read_bytes()
        return self.client.storage.from_(settings.supabase_bucket).download(path)
