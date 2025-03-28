Real-World Object Tracking with Gesture Recognition
This project is a real-time hand gesture recognition application that uses MediaPipe, OpenCV, and PyQt5 to track hand gestures and send the detected gestures to Unity via WebSocket. The application processes live video feed from a webcam, detects hand gestures, and displays the results on the GUI. It also communicates with Unity for further integration.

Features

Real-time hand tracking and gesture recognition using MediaPipe.
GUI built with PyQt5 for displaying the live video feed and detected gestures.
Gesture detection includes:
Swipe Left and Swipe Right (based on index finger movement).
Hi (Waving) gesture (based on wrist oscillation).
Like (Thumbs Up) and Dislike (Thumbs Down) gestures.
Fist and Open Hand detection.
Sends detected gestures to Unity via WebSocket for further processing.

Requirements

Before running the application, ensure you have the following installed:
Python 3.8 or higher
A webcam for live video feed

Installation and Setup

1. Clone the Repository
git clone https://github.com/your-username/Real-World-Object-Tracking.git
cd Real-World-Object-Tracking

2. Install Dependencies
Install the required Python libraries using the requirements.txt file:
pip install -r requirements.txt

3. Run the Application
Start the Python application:
python camera_app.py

How to Use

Launch the application.
The live video feed from your webcam will appear in the GUI.
Perform gestures in front of the camera:
Swipe Left: Move your index finger to the left.
Swipe Right: Move your index finger to the right.
Hi (Waving): Wave your hand left and right.
Like (Thumbs Up): Extend your thumb upward.
Dislike (Thumbs Down): Extend your thumb downward.
Fist: Close your hand into a fist.
Open Hand: Extend all fingers.
The detected gesture and hand state will be displayed on the GUI.
