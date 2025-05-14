# Hand-Gesture-Controller
Hand Gesture Controller
🖐️ Hand Gesture Controller
Control your computer like a wizard—just with your fingers!

This project uses computer vision and hand tracking to let you:

🎯 Control the mouse cursor

🔊 Adjust volume with pinching gestures

🖱️ Scroll through content with a hand flick

Built with OpenCV, MediaPipe, and PyAutoGUI, this system offers a hands-free way to interact with your computer in real-time.

🚀 Features
👆 Detects hand landmarks using MediaPipe

🖥️ Maps hand movements to cursor position

📜 Scrolls pages using finger distance

🔉 Adjusts system volume with gesture-based input

⚡ Smooth and real-time performance with FPS display

🧠 Modes & Gestures
Gesture	Mode Activated	Action

✊ All fingers down	Scroll Mode	Scrolls up/down based on finger spread

👉 Thumb + Index finger up	Volume Mode	Adjusts volume based on pinch distance

☝️ Only Index finger up	Cursor Mode	Moves cursor to match index finger

🛠️ Requirements
Install the required packages:

bash
Copy
Edit
pip install opencv-python mediapipe pyautogui numpy
📁 Project Structure
bash
Copy
Edit
.
├── HandGestureController.py        # Main script
├── HandTrackingModule.py           # Hand detection class using MediaPipe
└── README.md                       # You're here!
▶️ How to Run
bash
Copy
Edit
python HandGestureController.py
Press q to exit the application.

🧠 How It Works
Captures webcam input via OpenCV.

Detects hands using MediaPipe and extracts 21 hand landmarks.

Interprets gestures by analyzing landmark positions.

Performs corresponding actions using pyautogui:

Move cursor

Scroll window

Change volume

🧪 Example Use Cases
Control slides in a presentation

Browse the web hands-free

Assistive tech for accessibility

📸 Screenshot
Add a screenshot of the running application here showing the detected hand and mode display

🙌 Credits
OpenCV

MediaPipe

PyAutoGUI

📜 License
MIT License

