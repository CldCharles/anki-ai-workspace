from __future__ import annotations

from aqt import mw

from .diagnostics import configure_log, logger
from .profile_dialog import show_profile_dialog
from .reviewer import register as register_reviewer

_registered = False


def register() -> None:
    """Register the add-on's Anki UI hooks once per application session."""

    global _registered
    if _registered:
        return
    configure_log(mw.pm.base)
    logger().info("add-on registration started")
    action = mw.form.menuTools.addAction("AI Deck Profiles…")
    action.triggered.connect(show_profile_dialog)
    register_reviewer()
    _registered = True
    logger().info("add-on registration completed")
