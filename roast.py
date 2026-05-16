from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()  # reads your .env file

def get_roast(player_score, computer_score):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))  # reads from .env
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"You are a funny roaster. Score is Player:{player_score} - Computer:{computer_score}. In a rock paper scissors game. Roast the player in ONE short very funny sentence!"
            }
        ],
    )
    return response.choices[0].message.content