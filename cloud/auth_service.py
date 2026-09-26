"""Supabase Auth helper for trusted server-side code."""
from supabase import create_client

def create_auth_client(url: str, anon_key: str):
    return create_client(url, anon_key)
