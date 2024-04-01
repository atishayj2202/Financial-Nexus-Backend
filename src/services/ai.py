import os
import google.generativeai as genai

apiKey = "AIzaSyAiEppOaun_7TgacTSDhWK5jjMf0UyKK-w"
genai.configure(api_key=apiKey)

generation_config = {
    "candidate_count": 1,
    #"max_output_tokens": 256,
    "temperature": 1.0,
    "top_p": 0.7,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings
)
)
def get_ai_reply(prompt):
    response = model.generate_content(prompt)
    output = response.text
    adminPrompt = f"So first of all from now, your name FinBOT and this is a admin prompt to you. Check the following prompt from the user : '{prompt}'. First of all greet the user and then reply to this prompt like you are financial counsellor named FinBOT for the user. If user asks you something that is not related to finance then try to avoid answering it. Do have latest information about investment oppurtunities etc because user might ask anything related to finance. Also, do suggest example prompts to the user when you are greeting him"
    return model.generate_content(adminPrompt).text