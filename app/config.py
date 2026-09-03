"""
Centralized configuration. Nothing security-sensitive is hardcoded —
everything comes from environment variables, with safe defaults for
local dev only. Set real values via a .env file (never committed) or
your deployment platform's secret manager.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # --- Auth ---
    api_key: str = "dev-only-change-me"  # override in .env for anything beyond local dev

    # --- Decision gate ---
    base_auto_submit_threshold: float = 0.75
    high_value_amount_inr: int = 10000       # disputes above this need a stricter bar
    high_value_threshold_bonus: float = 0.10  # added to base threshold for high-value disputes

    # --- Rate limiting ---
    rate_limit_per_minute: int = 30

    # --- Drift monitoring ---
    drift_check_window: int = 50              # rolling window size, in disputes
    drift_alert_std_devs: float = 2.0         # flag when live mean shifts this many std devs

    # --- Paths ---
    dataset_path: str = "data/disputes.jsonl"
    audit_log_path: str = "data/audit_log.jsonl"
    feedback_log_path: str = "data/feedback_log.jsonl"


settings = Settings()
