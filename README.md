
```markdown
# 🚀 Space Hand Navigator – Gesture‑Controlled 3D Spaceship

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hands-orange?logo=google)
![Pygame](https://img.shields.io/badge/Pygame-2.x-red?logo=pygame)
![License](https://img.shields.io/badge/License-MIT-purple)

Control a **fully procedural, colored 3D spaceship** in a neon starfield using **just your hand**.  
No controllers. No external 3D models. Just your webcam, smooth hand tracking, and a cyber‑style UI. [web:24][web:40][web:93]

> 💡 The spaceship mesh, colors, and 3D engine are all written in pure Python with NumPy + Pygame. No `.obj` files required.

---

## ✨ Features

- ✋ **Real‑time hand tracking**
  - Uses **MediaPipe Hands** to track 21 landmarks directly from the webcam. [web:24][web:40]
- 🎮 **Gesture‑based control**
  - Move your **index finger** → rotate the ship in 3D
  - **Pinch (thumb + index)** → zoom the ship in and out
- 🌌 **Immersive space UI**
  - 300+ animated stars with trails
  - Depth‑based brightness for a warp‑speed effect
  - HUD with mode, warp speed, FPS, and mesh stats
- 🛸 **Custom 3D spaceship**
  - Procedural low‑poly ship with cockpit, wings, fin, and engines
  - **Per‑face colors** (hull, wings, engines) for a clean futuristic look
  - Edge glow and vertex highlights for a cyber aesthetic
- 🧊 **Smooth, stable motion**
  - Exponential smoothing on hand input
  - Per‑frame delta clamping to remove jitter and jumps [web:29][web:46]
- 🔁 **Auto / manual modes**
  - Manual: control with your hand
  - Auto: idle rotation showcase

---

## 🛠 Requirements

- Python **3.8+**
- A working webcam
- OS: Windows / macOS / Linux

### Python packages

```
opencv-python
mediapipe
pygame
numpy
```

Install them with:

```
pip install opencv-python mediapipe pygame numpy
```

---

## 🚀 Quick Start

1. **Clone the repo**

   ```
   git clone https://github.com/your-username/space-hand-navigator.git
   cd space-hand-navigator
   ```

2. (Optional) **Create and activate a virtual environment**

   ```
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```
   pip install opencv-python mediapipe pygame numpy
   ```

4. **Run the app**

   ```
   python main.py
   ```

On first run, allow camera access if your OS asks.

---

## 🕹 Controls

| Action                | Input                                  |
|-----------------------|----------------------------------------|
| Rotate spaceship      | Move your **index fingertip**         |
| Zoom in / out         | **Pinch** (thumb + index)             |
| Toggle auto‑rotate    | `SPACE`                                |
| Increase warp speed   | `↑` (Up arrow)                         |
| Decrease warp speed   | `↓` (Down arrow)                       |
| Reset smoothing       | `R`                                    |
| Quit                  | `ESC`                                  |

HUD elements:
- Top‑left: title + controls
- Bottom‑left: mode (AUTO/MANUAL), warp speed, vertex/face count
- Top‑right: FPS indicator (green = smooth, red = low)

---

## 💡 How It Works (High Level)

### Hand tracking and gestures

- Frames are captured from the webcam using OpenCV (`cv2.VideoCapture`). [web:24][web:94]  
- **MediaPipe Hands** runs on each frame and returns normalized hand landmarks. [web:40][web:41]
- The script uses:
  - Landmark **8** (index fingertip) → horizontal and vertical position
  - Landmark **4** (thumb tip) and **8** → pinch distance

### Smoothing for better UI

- Raw `x`, `y`, and pinch values go through **exponential moving average** smoothers.
- Rotations and scale are then smoothed again and **clamped** per frame so they cannot change too fast.
- This removes jitter and prevents “teleporting” when tracking briefly glitches. [web:29][web:46]

### 3D engine and visuals

- The spaceship is defined in `create_spaceship_mesh()` as:
  - A list of 3D vertices
  - A list of faces (triangles using vertex indices)
  - A per‑face color array (different palettes for cockpit, hull, wings, engines) [web:59][web:62]
- The engine:
  - Applies rotation matrices (X, Y, Z)
  - Scales the mesh to fit nicely on screen
  - Projects 3D points to 2D via a simple perspective projection
  - Sorts faces by depth (painters algorithm) and draws colored polygons
  - Adds glowing edges and small vertex dots for a clean, readable UI
- The starfield is a minimal particle system with Z‑movement and respawn, giving a warp effect.

---

## 📁 Project Structure

```
space-hand-navigator/
├── main.py        # Full application: tracking + 3D rendering + UI
├── README.md      # Project documentation
└── requirements.txt (optional)
```

You can generate `requirements.txt` with:

```
pip freeze > requirements.txt
```

---

## 🌟 Possible Extensions

- Add more gestures (e.g. fist to fire lasers or trigger effects). [web:52][web:99]  
- Add sound effects with `pygame.mixer` for engine hums or UI beeps. [web:92]  
- Support multiple ships or camera modes (chase cam, top‑down, etc.).  
- Export the procedural mesh to a `.obj` file for use in other engines.

---

## 📜 License

This project is licensed under the **MIT License**.  
You are free to use, modify, and share it in your own projects.

---

## 🙌 Built With

- **OpenCV** – real‑time video capture and image processing [web:24][web:94]  
- **MediaPipe Hands** – ML‑powered hand landmark detection [web:40][web:41]  
- **Pygame** – windowing, drawing, fonts, and main loop [web:92]  
- **NumPy** – fast math for 3D transforms [web:59][web:62]

> “In this cockpit, your hand is the only controller you need.”  
```
