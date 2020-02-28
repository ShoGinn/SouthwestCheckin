"""Global Variables.

By design, import no any other local module inside this file.
Vice verse, it'd produce circular dependent imports.
"""
from dataclasses import dataclass


@dataclass
class Config:
    """Globally accessible settings throughout the whole project."""

    base_url: str = 'https://mobile.southwest.com/api/'
    checkin_interval_seconds: float = 0.25
    max_attempts: int = 40


config: Config = Config()
