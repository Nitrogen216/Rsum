import os
from pathlib import Path


def load_dotenv(dotenv_path: str = ".env") -> None:
    """Load key=value pairs from a .env file into os.environ if not set.

    Minimal parser: ignores empty lines and lines starting with '#'.
    Supports unquoted or quoted values. Existing env vars are not overridden.
    """
    path = Path(dotenv_path)
    if not path.exists():
        return

    try:
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)
    except Exception:
        # Fail silently to avoid breaking caller flows; caller will validate presence.
        pass


def get_openai_api_key() -> str:
    """Return OPENAI_API_KEY after attempting to load from .env."""
    load_dotenv()
    return os.getenv("OPENAI_API_KEY", "")


def ensure_openai_api_key() -> str:
    """Fetch OPENAI_API_KEY or raise a clear error if missing."""
    key = get_openai_api_key()
    if not key:
        raise RuntimeError(
            "OPENAI_API_KEY not set. Create a .env with OPENAI_API_KEY=... or export it in your shell.")
    return key

