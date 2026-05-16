import cv2 as cv
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np 
import time
import random
from roast import get_roast

# ─── constants ───────────────────────────────────────
HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),
    (0,5),(5,6),(6,7),(7,8),
    (0,9),(9,10),(10,11),(11,12),
    (0,13),(13,14),(14,15),(15,16),
    (0,17),(17,18),(18,19),(19,20)
]

# ─── functions ───────────────────────────────────────
def computer_choice():
    choice = ["rock", "paper", "scissors"]
    return random.choice(choice)

def determine_winner(player, computer):
    if player == computer:
        return ["tie", computer, player]
    elif (player == "rock" and computer == "scissors") or \
         (player == "paper" and computer == "rock") or \
         (player == "scissors" and computer == "paper"):
        return ["You win!", computer, player]
    else:
        return ["Computer wins!", computer, player]

def gesture(hand_landmarks):
    if hand_landmarks[8].y < hand_landmarks[6].y and hand_landmarks[12].y < hand_landmarks[10].y and hand_landmarks[16].y < hand_landmarks[14].y and hand_landmarks[20].y < hand_landmarks[18].y:
        return "paper"
    if hand_landmarks[8].y < hand_landmarks[6].y and hand_landmarks[12].y < hand_landmarks[10].y:
        return "scissors"
    if hand_landmarks[8].y > hand_landmarks[6].y and hand_landmarks[12].y > hand_landmarks[10].y:
        return "rock"
    return "unknown"

def wrap_text(text, max_width, font, font_scale, thickness):
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        (width, _), _ = cv.getTextSize(test_line, font, font_scale, thickness)
        if width > max_width:
            lines.append(current_line)
            current_line = word + " "
        else:
            current_line = test_line
    lines.append(current_line)
    return lines

def draw_landmarks(frame, hand_landmarks):
    h, w, _ = frame.shape
    points = []
    for lm in hand_landmarks:
        x, y = int(lm.x * w), int(lm.y * h)
        points.append((x, y))
        cv.circle(frame, (x, y), 5, (0, 255, 0), -1)
    for start, end in HAND_CONNECTIONS:
        cv.line(frame, points[start], points[end], (255, 0, 0), 2)

def setup_detector():
    base_options = python.BaseOptions(
        model_asset_path='hand_landmarker.task'
    )
    settings = vision.HandLandmarkerOptions(
        base_options=base_options,
        num_hands=1,
        running_mode=vision.RunningMode.VIDEO
    )
    return vision.HandLandmarker.create_from_options(settings)

# ─── main ────────────────────────────────────────────
def main():
    detector = setup_detector()

    cap = cv.VideoCapture(0, cv.CAP_DSHOW)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    timestamp = 0
    state = "waiting"
    start_time = None
    current_gesture = "unknown"
    round_num = 1
    player_score = 0
    computer_score = 0
    comp_choice = ""
    result_text = ""
    locked_gesture = "unknown"
    result_start_time = None
    roast_text = ""
    lines = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        timestamp += 1
        detection = detector.detect_for_video(mp_image, timestamp)

        current_gesture = "unknown"
        if detection.hand_landmarks:
            for hand_landmark in detection.hand_landmarks:
                draw_landmarks(frame, hand_landmark)
                current_gesture = gesture(hand_landmark)

        h, w, _ = frame.shape
        black_panel = np.zeros((h, w, 3), dtype=np.uint8)

        if state == "waiting":
            cv.putText(black_panel, "Press S to start", (10, 30),
                       cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
            cv.putText(black_panel, f"Round: {round_num}/5", (10, 70),
                       cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

        elif state == "countdown":
            elapsed = time.time() - start_time
            remaining = int(3 - elapsed)
            cv.putText(black_panel, f"Round: {round_num}/5", (10, 30),
                       cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
            cv.putText(black_panel, f"Time: {remaining}", (10, 70),
                       cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
            cv.putText(black_panel, f"Gesture: {current_gesture}", (10, 110),
                       cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            if elapsed >= 3:
                locked_gesture = current_gesture
                comp_choice = computer_choice()
                result_text, _, _ = determine_winner(locked_gesture, comp_choice)
                if result_text == "You win!":
                    player_score += 1
                elif result_text == "Computer wins!":
                    computer_score += 1
                state = "result"
                result_start_time = time.time()

        elif state == "result":
            result_elapsed = time.time() - result_start_time
            cv.putText(black_panel, f"You played: {locked_gesture}",
                       (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
            cv.putText(black_panel, f"Computer played: {comp_choice}",
                       (10, 70), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
            cv.putText(black_panel, result_text,
                       (10, 110), cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            cv.putText(black_panel, f"Next round in: {int(3 - result_elapsed)}",
                       (10, 150), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

            if result_elapsed >= 3:
                if player_score == 3 or computer_score == 3 or round_num >= 5:
                    state = "gameover"
                else:
                    round_num += 1
                    state = "countdown"
                    start_time = time.time()

        elif state == "gameover":
            if roast_text == "":
                roast_text = get_roast(player_score, computer_score)
                lines = wrap_text(roast_text, black_panel.shape[1] - 20,
                                  cv.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv.putText(black_panel, "GAME OVER!", (10, 30),
                       cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            if player_score > computer_score:
                cv.putText(black_panel, "YOU WIN!", (10, 70),
                           cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            elif computer_score > player_score:
                cv.putText(black_panel, "COMPUTER WINS!", (10, 70),
                           cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            else:
                cv.putText(black_panel, "IT'S A TIE!", (10, 70),
                           cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)
            cv.putText(black_panel, f"Final: You {player_score} - {computer_score} Comp",
                       (10, 110), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
            cv.putText(black_panel, "Press Q to quit", (10, 150),
                       cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
            y_position = h - (len(lines) * 30) - 20
            for line in lines:
                cv.putText(black_panel, line, (10, y_position),
                           cv.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)
                y_position += 30

        combined = np.hstack((black_panel, frame))
        cv.imshow('RPS Game', combined)

        key = cv.waitKey(1)
        if key == ord('s'):
            if state == "waiting":
                state = "countdown"
                start_time = time.time()
        if key == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()