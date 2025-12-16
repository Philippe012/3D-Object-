# 🚀 Space Hand Navigator

<div align="center">

**Control a 3D spaceship through space using only your hand gestures**

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Hands-FF6F00?style=for-the-badge&logo=google&logoColor=white)](https://google.github.io/mediapipe/)
[![Pygame](https://img.shields.io/badge/Pygame-2.x-00A82D?style=for-the-badge&logo=python&logoColor=white)](https://www.pygame.org/)
[![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)](LICENSE)

![Demo GIF Placeholder](https://via.placeholder.com/800x400/0a0e27/00ff88?text=Space+Hand+Navigator+Demo)

</div>

---

## 🌟 Overview

Experience the future of interaction with **Space Hand Navigator** – a gesture-controlled 3D spaceship simulator built entirely in Python. Navigate through a stunning neon starfield using only your webcam and hand movements. No controllers, no VR headsets, just pure hand tracking technology.

### 🎯 What Makes It Special?

- **Zero External Models**: Every 3D element is procedurally generated in pure Python
- **Real-time Hand Tracking**: Powered by MediaPipe's state-of-the-art hand detection
- **Cyber Aesthetic**: Neon colors, glowing edges, and a sleek futuristic HUD
- **Smooth Performance**: Optimized rendering with intelligent motion smoothing

---

## ✨ Features

### 🖐️ Intuitive Hand Controls

| Gesture | Action |
|---------|--------|
| **Move Index Finger** | Rotate spaceship in 3D space |
| **Pinch (Thumb + Index)** | Zoom in/out |
| **Open Palm** | Reset to default view |

### 🎨 Visual Excellence

- **Dynamic Starfield**: 300+ animated stars with motion trails
- **Depth-Based Rendering**: Stars dim with distance for realistic depth perception
- **Warp Speed Effect**: Visual feedback creates an immersive space travel experience
- **Real-time HUD**: Displays FPS, warp speed, control mode, and mesh statistics

### 🛸 Custom 3D Spaceship

- **Procedural Generation**: Low-poly spaceship created entirely with NumPy arrays
- **Color-Coded Components**: 
  - 🔵 Hull (Blue-gray)
  - 🟢 Wings (Green)
  - 🔴 Engines (Red glow)
- **Visual Effects**: Edge highlighting and vertex glow for cyberpunk aesthetic

### ⚡ Performance Optimizations

- **Exponential Smoothing**: Eliminates jittery hand movements
- **Delta Clamping**: Prevents sudden jumps in camera position
- **Efficient Rendering**: Optimized projection and drawing pipeline

---

## 🚀 Quick Start

### Prerequisites

Ensure you have Python 3.8 or higher installed on your system.

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/space-hand-navigator.git
   cd space-hand-navigator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python space_navigator.py
   ```

### Dependencies

```
opencv-python>=4.5.0
mediapipe>=0.10.0
pygame>=2.0.0
numpy>=1.19.0
```

---

## 🎮 How to Play

1. **Launch the application** and position yourself in front of your webcam
2. **Raise your hand** with your palm facing the camera
3. **Move your index finger** to rotate the spaceship
4. **Pinch your thumb and index finger** together to zoom
5. Press **ESC** to exit

### 💡 Tips for Best Experience

- Ensure good lighting for optimal hand tracking
- Position yourself 2-3 feet from the camera
- Keep your hand clearly visible against the background
- Smooth, deliberate movements work better than quick gestures

---

## 🏗️ Project Structure

```
space-hand-navigator/
│
├── space_navigator.py      # Main application file
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── LICENSE                # MIT License
│
├── assets/                # (Optional) Screenshots/demos
│   └── demo.gif
│
└── docs/                  # (Optional) Additional documentation
    └── technical_details.md
```

---

## 🛠️ Technical Details

### Architecture

```
┌─────────────────┐
│   Webcam Feed   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ MediaPipe Hands │ ← Hand landmark detection (21 points)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Gesture Parser  │ ← Extract position, pinch distance
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Motion Smoother │ ← Exponential smoothing + delta clamping
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  3D Projection  │ ← NumPy-based perspective projection
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Pygame Renderer │ ← Draw spaceship, stars, HUD
└─────────────────┘
```

### Key Technologies

- **MediaPipe Hands**: 21-landmark hand tracking model
- **NumPy**: Fast matrix operations for 3D transformations
- **Pygame**: 2D rendering engine for drawing projected 3D points
- **OpenCV**: Webcam capture and image processing

---

## 🎨 Customization

### Modify Spaceship Colors

Edit the `get_face_color()` function in `space_navigator.py`:

```python
def get_face_color(face_idx, total_faces):
    # Customize your spaceship colors here
    if face_idx < 10:
        return (100, 120, 180)  # Hull
    elif face_idx < 20:
        return (80, 200, 120)   # Wings
    else:
        return (255, 80, 80)    # Engines
```

### Adjust Starfield Density

Change the `NUM_STARS` constant:

```python
NUM_STARS = 500  # Default is 300
```

### Tune Hand Sensitivity

Modify the smoothing factor:

```python
SMOOTH_FACTOR = 0.15  # Lower = smoother, Higher = more responsive
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. 🐛 **Report bugs** by opening an issue
2. 💡 **Suggest features** in the discussions
3. 🔧 **Submit pull requests** with improvements
4. 📖 **Improve documentation**

### Development Setup

```bash
# Fork and clone your fork
git clone https://github.com/YOUR_USERNAME/space-hand-navigator.git

# Create a feature branch
git checkout -b feature/amazing-feature

# Make your changes and commit
git commit -m "Add amazing feature"

# Push and create a pull request
git push origin feature/amazing-feature
```

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **MediaPipe Team** for the excellent hand tracking solution
- **Pygame Community** for the versatile rendering library
- **OpenCV Contributors** for computer vision tools

---

## 📧 Contact

**Your Name** - [@yourtwitter](https://twitter.com/yourtwitter)

Project Link: [https://github.com/yourusername/space-hand-navigator](https://github.com/yourusername/space-hand-navigator)

---

<div align="center">

**⭐ Star this repo if you found it helpful!**

Made with ❤️ and Python

</div>
