from data import ss_data
import pyscreenshot
import os

def take_screenshot():
    image = pyscreenshot.grab()
    dataset = ss_data()

    while 1:
        a = next(dataset)
        try:
            path = f"/home/codeaxon/Pictures/Screenshots/{a}.png"
        except:
            path = os.path.expanduser(f"~/Pictures/Screenshots/{a}.png")
        
        if not os.path.exists(path):
            break

    # Save the screenshot
    image.save(path)
    print(f"Screenshot saved at {path}")

