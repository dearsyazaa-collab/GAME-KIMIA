import cv2
import math
import sys
import threading

try:
    import mediapipe as mp
    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils
except Exception as e:
    print(f"Error initializing MediaPipe solutions: {e}")
    sys.exit(1)

class CameraTracker:
    def __init__(self, device_index=0):
        self.cap = cv2.VideoCapture(device_index)
        self.mp_hands = mp_hands
        self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
        self.mp_draw = mp_draw
        
        # Threading variables
        self.current_frame = None
        self.fingers_up = 0
        self.is_fire_pose = False
        self.is_pinching = False
        self.current_index_finger_pos = None
        self.is_running = False
        self.lock = threading.Lock()
        self.thread = None

    def _hitung_jarak(self, p1, p2):
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

    def start(self):
        self.is_running = True
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

    def run(self):
        while self.is_running:
            success, frame = self.cap.read()
            if not success:
                continue
                
            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = self.hands.process(rgb)
            
            # Reset values for each frame
            fingers = 0
            fire_pose = False
            pinch = False
            finger_pos = None
            
            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    lm = hand_landmarks.landmark
                    
                    thumb_tip, index_tip = lm[4], lm[8]
                    middle_tip, ring_tip, pinky_tip = lm[12], lm[16], lm[20]
                    index_pip, middle_pip = lm[6], lm[10]
                    ring_pip, pinky_pip = lm[14], lm[18]
                    
                    is_index_up = index_tip.y < index_pip.y
                    is_middle_up = middle_tip.y < middle_pip.y
                    is_ring_up = ring_tip.y < ring_pip.y
                    is_pinky_up = pinky_tip.y < pinky_pip.y
                    is_thumb_up = thumb_tip.y < lm[3].y

                    fingers = sum([is_index_up, is_middle_up, is_ring_up, is_pinky_up, is_thumb_up])
                    
                    # Pose Dua Jari untuk Api
                    fire_pose = (is_index_up and is_middle_up and not is_ring_up and not is_pinky_up)
                    
                    pinch = (self._hitung_jarak(thumb_tip, index_tip) < 0.06)
                    
                    finger_x = int(index_tip.x * 1000)
                    finger_y = int(index_tip.y * 700)
                    finger_pos = (finger_x, finger_y)
            
            with self.lock:
                self.current_frame = frame
                self.fingers_up = fingers
                self.is_fire_pose = fire_pose
                self.is_pinching = pinch
                self.current_index_finger_pos = finger_pos

    def stop(self):
        self.is_running = False
        if self.thread is not None:
            self.thread.join()
        self.cap.release()
