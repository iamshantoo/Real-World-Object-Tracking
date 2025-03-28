# Real-World Object Tracking with Gesture Recognition

This project is a **real-time hand gesture recognition** application that uses **MediaPipe, OpenCV, and PyQt5** to track hand gestures and send the detected gestures to Unity via WebSocket.  
It processes a **live video feed** from a webcam, detects hand gestures, and displays the results on the GUI. It also communicates with Unity for further integration.

---

## ✨ Features

- **Real-time hand tracking & gesture recognition** using MediaPipe.
- **GUI built with PyQt5** to display the live video feed and detected gestures.
- **Recognized Gestures:**
  - ✅ **Swipe Left** and **Swipe Right** (based on index finger movement).
  - 👋 **Hi (Waving)** (based on wrist oscillation).
  - 👍 **Like (Thumbs Up)** and 👎 **Dislike (Thumbs Down)**.
  - ✊ **Fist** and ✋ **Open Hand** detection.
- **WebSocket communication with Unity** for further processing.

---

## 📌 Requirements

Before running the application, ensure you have the following installed:

- ✅ **Python 3.8 or higher**
- ✅ **A webcam** for live video feed

---

## ⚙️ Installation and Setup

### 1️⃣ Clone the Repository  
Run the following command in your terminal:
```sh
git clone https://github.com/your-username/Real-World-Object-Tracking.git
cd Real-World-Object-Tracking
