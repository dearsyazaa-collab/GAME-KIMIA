import cv2
import mediapipe as mp
import math

class CameraTracker:
    def __init__(self, device_index=0):
        self.cap = cv2.VideoCapture(device_index)
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
        self.mp_draw = mp.solutions.drawing_utils

    def _hitung_jarak(self, p1, p2):
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

    def update(self):
        """Membaca /dev/video0, memproses MediaPipe, mengembalikan tuple (frame_rgb, pose_string)"""
        success, frame = self.cap.read()
        if not success:
            return None, "STANDBY"
            
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)
        
        pose_aktif = "STANDBY"
        
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                lm = hand_landmarks.landmark
                
                wrist = lm[0]
                thumb_tip, index_tip = lm[4], lm[8]
                middle_tip, ring_tip, pinky_tip = lm[12], lm[16], lm[20]
                index_pip, middle_pip = lm[6], lm[10]
                ring_pip, pinky_pip = lm[14], lm[18]
                
                is_index_up = index_tip.y < index_pip.y
                is_middle_up = middle_tip.y < middle_pip.y
                is_ring_up = ring_tip.y < ring_pip.y
                is_pinky_up = pinky_tip.y < pinky_pip.y

                if self._hitung_jarak(thumb_tip, index_tip) < 0.06:
                    pose_aktif = "SIHIR API"
                elif (is_index_up and is_middle_up and not is_ring_up and not is_pinky_up):
                    pose_aktif = "SIHIR ES"
                elif (not is_index_up and not is_middle_up and not is_ring_up and not is_pinky_up):
                    pose_aktif = "LOMPAT"
                elif is_index_up and is_pinky_up and not is_middle_up:
                    pose_aktif = "KUIS"
                else: 
                    pose_aktif = "JALAN"
                    
        return frame, pose_aktif

    def close(self):
        self.cap.release()
