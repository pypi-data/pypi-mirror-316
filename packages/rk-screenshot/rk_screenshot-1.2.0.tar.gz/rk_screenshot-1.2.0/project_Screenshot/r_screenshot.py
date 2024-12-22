import cv2
import mediapipe as mp
import time
from datetime import datetime
import pyscreenshot
import os

def take_screenshot():
    image = pyscreenshot.grab()
    
    # Generate a unique filename using timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    try:
        path = f"/home/codeaxon/Pictures/Screenshots/screenshot_{timestamp}.png"
    except:
        path = os.path.expanduser(f"~/Pictures/Screenshots/screenshot_{timestamp}.png")
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Save the screenshot
    image.save(path)
    print(f"Screenshot saved at {path}")


def capture_screenshot():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
    mp_draw = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0) 

    prev_state = None  

    def is_palm_open(landmarks):
        fingers = [8, 12, 16, 20]
        open_fingers = 0
        for finger in fingers:
            if landmarks[finger].y < landmarks[finger - 2].y:  # Compare with lower joints
                open_fingers += 1
        return open_fingers >= 4

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        # Convert image to RGB its necessary as mediapipe work on these RGB only
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_image)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = hand_landmarks.landmark
                if is_palm_open(landmarks):
                    current_state = "open"
                else:
                    current_state = "fist"

                if prev_state == "open" and current_state == "fist":
                    take_screenshot()

                prev_state = current_state

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    cap.release()

