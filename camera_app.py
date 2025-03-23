import sys
import cv2
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from gesture_tracking import GestureTracking  # Import the new GestureTracking class

class CameraApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Live Camera Feed")
        self.setGeometry(100, 100, 640, 480)

        # Layout
        self.layout = QVBoxLayout()
        self.video_label = QLabel(self)
        self.layout.addWidget(self.video_label)

        # Close Button
        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.close_app)
        self.layout.addWidget(self.close_button)

        self.setLayout(self.layout)

        # OpenCV Video Capture
        self.cap = cv2.VideoCapture(0)

        # Verify the resolution
        actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f"Camera resolution: {actual_width} x {actual_height}")

        # Initialize GestureTracking
        self.gesture_tracker = GestureTracking()

        # Timer to update frames
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert the frame to RGB (MediaPipe requires RGB input)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the frame with MediaPipe Hands
            results = self.gesture_tracker.hands.process(frame_rgb)

            # Process gestures
            frame, hand_state, gesture = self.gesture_tracker.process_frame(frame, results)

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
