import os

from supabase import Client, create_client

from src.api.dependencies.read_secret_manager import read_value


def get_supabase_key() -> str:
    """Get supabase key From SecretManager."""
    return read_value(name="supabase-key")


def supabase() -> Client:
    url: str = os.environ.get("SUPABASE_URL")
    key: str = get_supabase_key()
    """Define supabase client."""
    return create_client(url, key)
