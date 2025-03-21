import sys
import cv2
import numpy as np
import mediapipe as mp
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer

class CameraApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Live Camera Feed")
        self.setGeometry(100, 100, 640, 480)  # Set the window size to 640 x 480

        # Layout
        self.layout = QVBoxLayout()
        self.video_label = QLabel(self)  # QLabel to display video frames
        self.layout.addWidget(self.video_label)

        # Close Button
        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.close_app)
        self.layout.addWidget(self.close_button)

        self.setLayout(self.layout)

        # OpenCV Video Capture
        self.cap = cv2.VideoCapture(0)  # 0 = default webcam

        # Verify the resolution (use the default resolution provided by the camera)
        actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f"Camera resolution: {actual_width} x {actual_height}")

        # Timer to update frames
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Refresh rate: 30ms

        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False,
                                         max_num_hands=2,
                                         min_detection_confidence=0.5,
                                         min_tracking_confidence=0.5)
        self.mp_draw = mp.solutions.drawing_utils

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert the frame to RGB (MediaPipe requires RGB input)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the frame with MediaPipe Hands
            results = self.hands.process(frame_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw hand landmarks on the frame
                    self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                    # Get the frame dimensions
                    h, w, _ = frame.shape

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

                    for tip, base, name, color in zip(finger_tips, finger_bases, finger_names, finger_colors):
                        tip_landmark = hand_landmarks.landmark[tip]
                        base_landmark = hand_landmarks.landmark[base]

                        # Convert normalized coordinates to pixel values
                        tip_x, tip_y = int(tip_landmark.x * w), int(tip_landmark.y * h)
                        base_y = int(base_landmark.y * h)

                        # Check if the finger is extended (tip is farther from the palm than the base)
                        if tip_y < base_y:  # Lower y-coordinate means higher position
                            fingers_extended += 1

                            # Display the finger name and draw a circle at the fingertip
                            cv2.putText(frame, name, (tip_x, tip_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
                            cv2.circle(frame, (tip_x, tip_y), 10, color, -1)  # Draw a circle at the fingertip

                    # Determine the hand state
                    if fingers_extended == 0:
                        hand_state = "Closed (Fist)"
                    elif fingers_extended == 5:
                        hand_state = "Open"
                    else:
                        hand_state = "Partially Open"

                    # Recognize gestures based on the number of fingers extended
                    if fingers_extended == 0:
                        gesture = "Fist"
                    elif fingers_extended == 1:
                        gesture = "Pointing"
                    elif fingers_extended == 2:
                        gesture = "Peace"
                    elif fingers_extended == 5:
                        gesture = "Open Hand"
                    else:
                        gesture = f"{fingers_extended} Fingers Extended"

                    # Display the hand state and gesture on the frame
                    cv2.putText(frame, f"Hand State: {hand_state}", (25, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                    cv2.putText(frame, f"Gesture: {gesture}", (25, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            # Convert frame to RGB for displaying in QLabel
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape
            bytes_per_line = ch * w
            convert_to_qt = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(convert_to_qt))

    def close_app(self):
        self.cap.release()
        self.timer.stop()
        cv2.destroyAllWindows()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraApp()
    window.show()
    sys.exit(app.exec_())
