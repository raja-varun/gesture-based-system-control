# Gesture Based System Control

## 📌 Project Overview

Gesture Based System Control is a computer vision application that allows users to control system functions using hand gestures detected through a webcam.

Instead of using traditional input devices such as a mouse or keyboard, this system uses **hand gestures to control system volume, screen brightness, and scrolling**.

The project uses **MediaPipe for hand tracking** and **OpenCV for real-time video processing**, enabling natural human-computer interaction.

---

## 🎯 Features

* 🎵 Control **system volume** using finger distance gestures
* 💡 Adjust **screen brightness** using hand gestures
* 📜 **Scroll up and down** using palm position
* 🖐 Real-time **hand detection and tracking**
* 🔄 Automatic **gesture mode switching**
* ⚡ Fast and responsive **real-time processing**

---

## ✋ Gesture Controls

| Gesture           | Function                             |
| ----------------- | ------------------------------------ |
| 👍 Thumbs Up      | Activate **Brightness Control Mode** |
| ✌ Scissor Gesture | Activate **Volume Control Mode**     |
| ✊ Fist Gesture    | Activate **Scroll Mode**             |

---

## 🛠 Technologies Used

* **Python**
* **OpenCV**
* **MediaPipe**
* **NumPy**
* **PyAutoGUI**
* **PyCaw (Volume Control)**
* **Screen Brightness Control**

---

## 📂 Project Structure

```
Gesture-Based-System-Control
│
├── prototype1.py
├── requirements.txt
└── README.md
```

---

## ⚙ Installation

### 1️⃣ Clone the Repository

```
git clone https://github.com/your-username/gesture-based-system-control.git
cd gesture-based-system-control
```

### 2️⃣ Install Required Libraries

```
pip install opencv-python mediapipe numpy pyautogui screen-brightness-control pycaw comtypes
```

---

## ▶ Running the Project

Run the following command:

```
python prototype1.py
```

Your webcam will open and start detecting hand gestures.

Press **Q** to exit the program.

---

## 🖥 How It Works

1. The webcam captures live video.
2. MediaPipe detects **hand landmarks (21 points)**.
3. The system identifies specific **hand gestures**.
4. Each gesture activates a **control mode**:

   * Volume
   * Brightness
   * Scroll
5. The corresponding system function is adjusted in real time.

---

## 🚀 Future Improvements

* Add **more gesture controls**
* Support **multi-hand gestures**
* Improve gesture accuracy using **deep learning**
* Convert the project into a **standalone Windows application**

---

## 👨‍💻 Authors

**Raja Varun**
B.Tech Computer Science (Data Science)

**Madhavaram Vineel**

---

## 🎓 Academic Project

This project was developed as a **Real-Time Project for B.Tech Computer Science (Data Science)**.

Guided by:

* **K. Kotaiah Swamy**
* **Mr. Sunil Moses**
