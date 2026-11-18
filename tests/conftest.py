import sys
import os

# Ensure repository root is on sys.path for imports like `bot.*`
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


# pyautogui (via mouseinfo) reads os.environ['DISPLAY'] at import time, so importing the
# bot modules raises KeyError on a headless machine. CI and the Docker image supply a
# virtual display with xvfb-run; elsewhere, fall back to a stub so collection works.
# Tests never need real input events: they patch e.g. `bot.camera.pyautogui.scroll`.
try:
    import pyautogui  # noqa: F401
except Exception:  # KeyError: 'DISPLAY' headless; other import-time display errors too
    from unittest.mock import MagicMock

    sys.modules.pop("pyautogui", None)
    sys.modules["pyautogui"] = MagicMock(name="pyautogui")
