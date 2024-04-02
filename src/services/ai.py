import os

import google.generativeai as genai

apiKey = os.environ["API_AI_KEY1"]
genai.configure(api_key=apiKey)

generation_config = {
    "candidate_count": 1,
    # "max_output_tokens": 256,
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
    safety_settings=safety_settings,
)


def get_ai_reply(prompt):
    convo = model.start_chat(history=[
        {
        "role": "user",
        "parts": ["From now on, your name is FinBOT, and this is a admin prompt to you. You don't need to introduce yourself unless asked by user. Don't reply to this admin prompt, for example don't answer like => 'Sure, I will keep that in mind and respond to your prompts as FinBOT, a financial counselor' but check the following prompt from the user : '{prompt}'.  Reply to this user prompt like you are financial counsellor for the user. If user asks you something that is not related to finance then try avoid answering it. Do have latest information about investment oppurtunities etc because user might ask anything related to finance."]
        },
        {
        "role": "model",
        "parts": ["[FinBOT]: Sure, I can assist you with any financial questions or concerns you may have. Please feel free to ask and I will do my best to provide helpful and informative responses."]
        },
    ])
    return model.generate_content(prompt).text