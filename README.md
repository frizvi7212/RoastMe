# RoastMe - Hand Gesture Rock Paper Scissors
# Demo Video: https://youtu.be/tUtIYX4m6Jc?si=1BXlqGXMddzL4E5B
#### Description:

## What is this project?

RoastMe is a Rock Paper Scissors game that uses your webcam to detect
hand gestures in real time using computer vision. You play against the
computer for 5 rounds and whoever wins 3 rounds first wins the game.
The twist? An AI roasts you at the end of every game based on your performance!

## How to Play

1. Run `project.py`
2. A split screen window opens — camera on the right, game info on the left
3. Press **S** to start the first round
4. Show your hand gesture to the camera within 3 seconds:
   - ✊ Fist = Rock
   - 🖐 Open hand = Paper
   - ✌️ Two fingers = Scissors
5. The game automatically moves to the next round
6. First to win 3 rounds wins the game
7. At the end the AI roasts you based on your score!
8. Press **Q** to quit

## Files

**project.py** - The main file where everything comes together. Contains
the camera loop, MediaPipe hand detection, game states (waiting, countdown,
result, gameover), and all the core functions like `gesture()`,
`determine_winner()`, `computer_choice()` and `wrap_text()`.

**roast.py** - Contains the `get_roast()` function which calls the Groq API
with the final score and gets back a funny one-liner roast to display at
the end of the game.

**test_project.py** - Contains pytest tests for the three main functions.
Uses mock/fake landmark objects to test gesture detection without needing
a real camera or MediaPipe running.

**requirements.txt** - Lists all the external libraries needed to run the
project. Install them all with `pip install -r requirements.txt`.

**hand_landmarker.task** - The MediaPipe hand detection model file. Required
for hand landmark detection to work.

## Libraries Used

- **OpenCV** → Handles the camera feed, drawing landmarks, text on screen
  and combining the split screen panels
- **MediaPipe** → Detects the hand and gives us 21 landmark positions on
  the hand which we use to figure out the gesture
- **Groq** → Free AI API used to generate funny roasts at the end of the game
- **NumPy** → Used to create the black panel on the left side of the screen

## Setup

1. Get a free Groq API key from https://console.groq.com
2. Create a `.env` file in the project folder
3. Add this line to it:
   GROQ_API_KEY=your_key_here
4. Run `pip install -r requirements.txt`
5. Run `python project.py`

## Design Choices

**Why states?**
The game needed to behave differently at different times — waiting for
input, running a countdown, showing results, and game over. Using a state
variable like `"waiting"`, `"countdown"`, `"result"` and `"gameover"` made
it easy to control what happens in each situation without messy if/else
chains everywhere. Each state has one clear job.

**Why MediaPipe?**
MediaPipe was the most straightforward library for real time hand detection
in Python. It gives back 21 precise landmark positions on the hand which
made it easy to check finger positions and classify gestures. Other options
like training a custom model would have been far too complex for this project.

**Why Groq API?**
Groq offers a free tier which made it perfect for this project. It supports
large language models like LLaMA which are capable of generating funny and
creative roasts. The API is also very simple to use and similar in structure
to other AI APIs so it was easy to integrate.

**Challenges faced**
The hardest part was understanding how MediaPipe landmark coordinates work.
The y axis increases downward on screen which is the opposite of what you
might expect, so figuring out the correct comparisons for finger up/down
detection took some trial and error. Writing tests for gesture detection was
also tricky since you can't use a real camera in tests — the solution was
creating fake landmark objects with just a `.y` attribute to simulate real
MediaPipe landmarks.

## How I Approached This Project

I broke this project down into small steps instead of trying to build
everything at once:

1. **Camera Connection** - First I got the webcam working using OpenCV
   and made sure I could display a live feed on screen.

2. **Hand Detection** - Then I added MediaPipe to detect the hand and
   draw the 21 landmarks on it. This took some time to understand how
   the new MediaPipe API works since the older tutorials online use a
   different syntax.

3. **Gesture Detection** - Once I could see the landmarks I wrote logic
   to classify the hand as Rock, Paper or Scissors by comparing the y
   positions of fingertips to their base joints.

4. **Basic Game Logic** - I wrote a simple Rock Paper Scissors game in
   plain Python first with just terminal input to make sure the win/loss
   logic worked correctly before touching the camera code.

5. **Connecting Camera to Game** - I then replaced the terminal input
   with the detected gesture from the camera.

6. **Round System** - Added 5 rounds with automatic advancement using
   a timer instead of waiting for key presses.

7. **Score Tracking** - Added score tracking and win conditions — first
   to 3 wins or whoever leads after 5 rounds.

8. **AI Roast** - Finally added the Groq API to generate a funny roast
   at the end based on the final score.

Building it step by step made the project much less overwhelming and made
debugging easier since each piece worked before moving to the next.
