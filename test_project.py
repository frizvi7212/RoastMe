from project import gesture, determine_winner, computer_choice

class FakeLandmark:
    def __init__(self, y):
        self.y = y

def test_gesture():
    # build fake rock hand
    rock_hand = [FakeLandmark(0)] * 21
    rock_hand[6]  = FakeLandmark(0.3)  
    rock_hand[8]  = FakeLandmark(0.8)  
    rock_hand[10] = FakeLandmark(0.3)  # middle pip
    rock_hand[12] = FakeLandmark(0.8)  # middle tip DOWN
    rock_hand[14] = FakeLandmark(0.3)  # ring pip
    rock_hand[16] = FakeLandmark(0.8)  # ring tip DOWN
    rock_hand[18] = FakeLandmark(0.3)  # pinky pip
    rock_hand[20] = FakeLandmark(0.8)  # pinky tip DOWN
    assert gesture(rock_hand) == "rock"

def test_determine_winner():
    assert determine_winner("rock", "scissors")[0] == "You win!"
    assert determine_winner("rock", "paper")[0] == "Computer wins!"
    assert determine_winner("rock", "rock")[0] == "tie"

def test_computer_choice():
    result = computer_choice()
    assert result in ["rock", "paper", "scissors"]