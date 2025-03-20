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
        self.setGeometry(100, 100, 640, 480)

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

                    # Example: Get the coordinates of the index finger tip (landmark 8)
                    index_finger_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    h, w, _ = frame.shape
                    cx, cy = int(index_finger_tip.x * w), int(index_finger_tip.y * h)

                    # Draw a circle at the index finger tip
                    cv2.circle(frame, (cx, cy), 10, (255, 0, 0), -1)

                    # Example: Display gesture (e.g., "Index Finger Detected")
                    cv2.putText(frame, "Index Finger Detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

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
