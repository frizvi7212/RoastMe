# ✊🖐✌️ RoastMe

> A Rock Paper Scissors game that uses your webcam to detect hand gestures 
> in real time and roasts you with AI at the end!

![Python](https://img.shields.io/badge/Python-3.14-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10-orange)
![Groq](https://img.shields.io/badge/AI-Groq-purple)

---

## 🎬 Demo
 [Watch Demo Video] https://youtu.be/tUtIYX4m6Jc

---

## 📖 What is this?

RoastMe is a Rock Paper Scissors game where instead of typing your move 
you just show your hand to the camera. The game detects whether you're 
showing Rock, Paper or Scissors using computer vision and plays against 
the computer. After 5 rounds the AI roasts you based on how you played!

Built as my CS50P final project after learning OpenCV and MediaPipe 
from scratch in about a week.

## 🚀 How to Run
1. Clone the repo
2. Install dependencies:
   pip install -r requirements.txt
3. Add your Groq API key in `.env`:
   GROQ_API_KEY=your_key_here
4. Run:
   python project.py

## 🎯 How to Play
| Gesture | Hand |
|---------|------|
| Rock    | ✊ Fist |
| Paper   | 🖐 Open hand |
| Scissors| ✌️ Two fingers |

- Press **S** to start
- Show gesture in 3 seconds
- First to 3 wins!
- AI roasts you at the end 😂

## 🛠️ Built With
- OpenCV — camera and display
- MediaPipe — hand detection
- Groq API — AI roasting
- NumPy — screen layout

## ⚙️ How It Works

1. OpenCV opens your webcam
2. Each frame is sent to MediaPipe which detects 21 landmarks on your hand
3. The game compares fingertip positions to base positions to classify the gesture
4. Game logic handles rounds, scoring and state management
5. At game over Groq API generates a roast based on your final score

---

## 📝 Notes

- Requires a webcam
- Works best with good lighting
- Make sure no other app is using your camera
