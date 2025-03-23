import numpy as np
import mediapipe as mp
import cv2  # Required for drawing circles and text

class GestureTracking:
    def __init__(self):
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False,
                                         max_num_hands=1,
                                         min_detection_confidence=0.5,
                                         min_tracking_confidence=0.5)
        self.mp_draw = mp.solutions.drawing_utils

        # Buffers to store x-coordinates for movement detection
        self.index_x_buffer = []  # For swipe detection
        self.wrist_x_buffer = []  # For waving detection
        self.buffer_size = 10  # Number of frames to track

    def process_frame(self, frame, results):
        h, w, _ = frame.shape
        gesture = "Unknown"
        hand_state = "Unknown"

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks on the frame
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                # Define finger tip and base landmarks
                finger_tips = [
                    self.mp_hands.HandLandmark.THUMB_TIP,
                    self.mp_hands.HandLandmark.INDEX_FINGER_TIP,
                    self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                    self.mp_hands.HandLandmark.RING_FINGER_TIP,
                    self.mp_hands.HandLandmark.PINKY_TIP,
                ]
                finger_bases = [
                    self.mp_hands.HandLandmark.THUMB_CMC,
                    self.mp_hands.HandLandmark.INDEX_FINGER_MCP,
                    self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP,
                    self.mp_hands.HandLandmark.RING_FINGER_MCP,
                    self.mp_hands.HandLandmark.PINKY_MCP,
                ]
                finger_names = ["Thumb", "Index", "Middle", "Ring", "Pinky"]

                # Define colors for each finger
                finger_colors = [
                    (255, 0, 0),  # Blue for Thumb
                    (0, 255, 0),  # Green for Index
                    (0, 0, 255),  # Red for Middle
                    (255, 255, 0),  # Cyan for Ring
                    (255, 0, 255),  # Magenta for Pinky
                ]

                # Count fingers that are extended
                fingers_extended = 0
                for tip, base in zip(finger_tips, finger_bases):
                    tip_landmark = hand_landmarks.landmark[tip]
                    base_landmark = hand_landmarks.landmark[base]

                    # Convert normalized coordinates to pixel values
                    tip_y = int(tip_landmark.y * h)
                    base_y = int(base_landmark.y * h)

                    # Check if the finger is extended
                    if tip_y < base_y:
                        fingers_extended += 1

                # Determine the hand state
                if fingers_extended == 0:
                    hand_state = "Closed (Fist)"
                elif fingers_extended == 5:
                    hand_state = "Open"
                else:
                    hand_state = "Partially Open"

                # Display fingertip names and circles only if the hand is open
                if hand_state == "Open":
                    for tip, name, color in zip(finger_tips, finger_names, finger_colors):
                        tip_landmark = hand_landmarks.landmark[tip]

                        # Convert normalized coordinates to pixel values
                        tip_x, tip_y = int(tip_landmark.x * w), int(tip_landmark.y * h)

                        # Draw a circle and display the finger name
                        cv2.circle(frame, (tip_x, tip_y), 10, color, -1)  # Draw a circle at the fingertip
                        cv2.putText(frame, name, (tip_x, tip_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

                # Recognize gestures based on the number of fingers extended
                if fingers_extended == 0:
                    gesture = "Fist"
                elif fingers_extended == 1:
                    # Detect Like (Thumbs Up) and Dislike (Thumbs Down)
                    thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
                    thumb_ip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_IP]
                    thumb_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_MCP]

                    thumb_tip_y = int(thumb_tip.y * h)
                    thumb_ip_y = int(thumb_ip.y * h)
                    thumb_mcp_y = int(thumb_mcp.y * h)

                    if thumb_tip_y < thumb_ip_y < thumb_mcp_y:  # Thumb pointing up
                        gesture = "Like (Thumbs Up)"
                    elif thumb_tip_y > thumb_ip_y > thumb_mcp_y:  # Thumb pointing down
                        gesture = "Dislike (Thumbs Down)"
                    else:
                        gesture = "Pointing"
                elif fingers_extended == 5:
                    # Detect waving (Hi gesture) and swiping gestures
                    wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
                    index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]

                    wrist_x = int(wrist.x * w)
                    index_x = int(index_tip.x * w)

                    # Add wrist x-coordinate to buffer for waving
                    self.wrist_x_buffer.append(wrist_x)
                    if len(self.wrist_x_buffer) > self.buffer_size:
                        self.wrist_x_buffer.pop(0)

                    # Add index x-coordinate to buffer for swiping
                    self.index_x_buffer.append(index_x)
                    if len(self.index_x_buffer) > self.buffer_size:
                        self.index_x_buffer.pop(0)

                    # Detect oscillation for waving
                    if len(self.wrist_x_buffer) == self.buffer_size:
                        movement_range = max(self.wrist_x_buffer) - min(self.wrist_x_buffer)
                        if movement_range > 50:  # Threshold for significant movement
                            gesture = "Hi (Waving)"
                        else:
                            gesture = "Open Hand"

                    # Detect swipe gestures based on index finger movement
                    if len(self.index_x_buffer) == self.buffer_size:
                        if self.index_x_buffer[-1] - self.index_x_buffer[0] > 70:  # Significant rightward movement
                            gesture = "Swipe Right"
                        elif self.index_x_buffer[0] - self.index_x_buffer[-1] > 70:  # Significant leftward movement
                            gesture = "Swipe Left"
                else:
                    gesture = f"{fingers_extended} Fingers Extended"

        return frame, hand_state, gesture