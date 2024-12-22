import importlib.resources
from playsound import playsound

def play_sound():
    """Play the shutter.mp3 sound from the package."""
    with importlib.resources.path("rk_screenshot", "shutter.mp3") as sound_path:
        playsound(str(sound_path))
