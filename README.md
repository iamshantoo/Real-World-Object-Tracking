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
```
---

## 2️⃣ Install Dependencies
Use pip to install the required Python libraries:
```sh
pip install -r requirements.txt
```

---

## 3️⃣ Run the Application
Execute the following command to start the Python application:
```sh
python camera_app.py
```

---

## 🎮 How to Use
- Launch the application.

- The live video feed from your webcam will appear in the GUI.

- Perform gestures in front of the camera:

  - 👉 Swipe Left: Move your index finger to the left.

  - 👈 Swipe Right: Move your index finger to the right.

  - 👋 Hi (Waving): Wave your hand left and right.

  - 👍 Like (Thumbs Up): Extend your thumb upward.

  - 👎 Dislike (Thumbs Down): Extend your thumb downward.

  - ✊ Fist: Close your hand into a fist.

  - ✋ Open Hand: Extend all fingers.

- The detected gesture and hand state will be displayed on the GUI.

- Unity will receive the gesture data via WebSocket.

---

## Unity Integration
To integrate with Unity, follow these steps:
### 1️⃣ Install WebSocketSharp in Unity
- Download the WebSocketSharp library.
- Add the WebSocketSharp.dll to your Unity project.

---

### 2️⃣ Create a WebSocket Server in Unity
Add the following script to a GameObject in Unity to set up a WebSocket server:
```sh
using System;
using WebSocketSharp;
using WebSocketSharp.Server;
using UnityEngine;

public class GestureWebSocket : MonoBehaviour
{
    private WebSocketServer wss;

    void Start()
    {
        // Start WebSocket server on port 8080
        wss = new WebSocketServer("ws://localhost:8080");
        wss.AddWebSocketService<GestureBehavior>("/Gesture");
        wss.Start();
        Debug.Log("WebSocket server started on ws://localhost:8080/Gesture");
    }

    void OnDestroy()
    {
        if (wss != null)
        {
            wss.Stop();
            wss = null;
        }
    }
}

public class GestureBehavior : WebSocketBehavior
{
    protected override void OnMessage(MessageEventArgs e)
    {
        // Log the received gesture
        Debug.Log($"Received gesture: {e.Data}");

        // Optionally, send a response back to the client
        Send($"Gesture {e.Data} received by Unity!");
    }
}

```

### 3️⃣ Run Unity
- Start the Unity project.
- Ensure the WebSocket server is running and listening on
  ```sh
  ws://localhost:8080/Gesture
  ```

---

## ⚙ Dependencies
The project uses the following Python libraries:
- **OpenCV**: For video capture and frame processing.
- **MediaPipe**: For hand tracking and gesture recognition.
- **PyQt5**: For building the GUI.
- **websocket-client**: For websocket communication with Unity.

---
