"""Cloud storage boundary used by the backend storage service."""
from supabase import create_client

def create_storage_client(url: str, service_role_key: str):
    return create_client(url, service_role_key)
