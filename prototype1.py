import cv2
import numpy as np
import mediapipe as mp
import pyautogui
import screen_brightness_control as sbc
from ctypes import POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import time

# Initialize MediaPipe Hand Detection
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Audio Setup
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

# Gesture Modes
MODES = {
    "volume": {"color": (0, 255, 0)},       # Green
    "brightness": {"color": (0, 0, 255)},   # Blue
    "scroll": {"color": (255, 0, 0)},       # Red
    "inactive": {"color": (100, 100, 100)}  # Gray
}
current_mode = "inactive"
last_mode_switch_time = 0  
message = ""
message_time = 0  

# Capture Setup
cap = cv2.VideoCapture(0)

def draw_level_bar(frame, level, label, position, color):
    """Draws volume and brightness level bars."""
    bar_x, bar_y = position
    cv2.rectangle(frame, (bar_x, bar_y), (bar_x + 20, bar_y + 200), (255, 255, 255), 2)
    fill = int((level / 100) * 200)
    cv2.rectangle(frame, (bar_x, bar_y + 200 - fill), (bar_x + 20, bar_y + 200), color, -1)
    cv2.putText(frame, f"{label}: {int(level)}%", (bar_x - 10, bar_y + 220), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

def display_message(frame):
    """Displays activation/deactivation messages for 2 seconds."""
    global message, message_time
    if time.time() - message_time < 2:  
        cv2.putText(frame, message, (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

def detect_gesture(landmarks, w, h):
    """Detects hand gestures for switching modes."""
    global current_mode, last_mode_switch_time, message, message_time

    # Get key points
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    ring_tip = landmarks[16]
    pinky_tip = landmarks[20]
    wrist = landmarks[0]

    # Calculate distances
    thumb_index_dist = np.linalg.norm([thumb_tip.x - index_tip.x, thumb_tip.y - index_tip.y])
    index_middle_dist = np.linalg.norm([index_tip.x - middle_tip.x, index_tip.y - middle_tip.y])

    # **Prevent Rapid Switching (1.5 sec delay)**
    if time.time() - last_mode_switch_time < 1.5:
        return  

    new_mode = None

    # **Gesture Detection for Mode Switching**
    if (thumb_tip.y < index_tip.y and thumb_tip.y < middle_tip.y and
        thumb_tip.y < ring_tip.y and thumb_tip.y < pinky_tip.y):
        new_mode = "brightness"  # Thumbs Up Gesture 🖐️

    elif index_middle_dist > 0.1 and thumb_index_dist > 0.2:
        new_mode = "volume"  # Scissor Gesture ✌️

    elif all(landmark.y > wrist.y for landmark in [thumb_tip, index_tip, middle_tip, ring_tip, pinky_tip]):
        new_mode = "scroll"  # Fist Gesture ✊

    # **Update Mode and Show Message**
    if new_mode and new_mode != current_mode:
        current_mode = new_mode
        message = f"{current_mode.upper()} Mode Activated"
        message_time = time.time()
        last_mode_switch_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    # **Reset to Inactive Mode if No Hands Detected for 3 Seconds**
    if not results.multi_hand_landmarks and time.time() - last_mode_switch_time > 3:
        if current_mode != "inactive":
            message = f"{current_mode.upper()} Mode Deactivated"
            message_time = time.time()
        current_mode = "inactive"

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            landmarks = hand_landmarks.landmark
            h, w, _ = frame.shape

            # **Detect Gesture for Mode Switching**
            detect_gesture(landmarks, w, h)

            # **Show Active Mode**
            cv2.putText(frame, f"Mode: {current_mode.upper()}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, MODES[current_mode]["color"], 2)

            # **Mode-Specific Actions**
            if current_mode != "inactive":
                thumb_tip = landmarks[4]
                index_tip = landmarks[8]
                middle_tip = landmarks[12]
                palm = landmarks[0]

                thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
                index_x, index_y = int(index_tip.x * w), int(index_tip.y * h)
                palm_y = int(palm.y * h)

                if current_mode == "volume":
                    dist = np.linalg.norm([thumb_x - index_x, thumb_y - index_y])
                    vol_level = np.interp(dist, [30, 150], [0, 100])
                    volume.SetMasterVolumeLevel(np.interp(dist, [30, 150], [-65.25, 0]), None)
                    draw_level_bar(frame, vol_level, "Volume", (50, 50), MODES["volume"]["color"])

                elif current_mode == "brightness":
                    dist = np.linalg.norm([index_x - middle_tip.x * w, index_y - middle_tip.y * h])
                    brightness = np.interp(dist, [20, 200], [10, 100])
                    sbc.set_brightness(int(brightness))
                    draw_level_bar(frame, brightness, "Brightness", (100, 50), MODES["brightness"]["color"])

                elif current_mode == "scroll":
                    if palm_y < h // 3:
                        pyautogui.scroll(20)
                    elif palm_y > 2 * h // 3:
                        pyautogui.scroll(-20)

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # **Show Activation/Deactivation Messages**
    display_message(frame)

    cv2.imshow("Gesture Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
