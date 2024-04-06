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

def aimodel(prompt: str, asset: list, bank: list, card: list, emi: list, loan: list, stock: list):
    
    if(len(bank)==0):
        bank_prompt = "User has not listed any bank account."
    elif(len(bank)>0):
        bank_prompt = f"User has a bank account in {bank[0]['bank_name']} with Rs. {bank[0]['balance']} balance. He can refer this account by the name  {bank[0]['name']} "
        if(len(bank)>1):
            for i in range(1, len(bank)):
                bank_prompt = bank_prompt + f"Also, user has a bank account in {bank[i]['bank_name']} with Rs. {bank[i]['balance']} balance. He can refer this account by the name  {bank[i]['name']} "
    if(len(asset)==0):
        asset_prompt = "User has not listed any asset."
    elif(len(asset)>0):
        asset_prompt = f"User has a asset named {asset[0]['name']} with {asset[0]['initial_amount']} value "
        if(len(asset)>1):
            for i in range(1, len(asset)):
                asset_prompt = asset_prompt + f"Also, user has a asset named {asset[i]['name']} with Rs. {asset[i]['initial_amount']} worth of value "
    
    if(len(card)==0):
        card_prompt = "User has not listed any credit card."
    elif(len(card)>0):
        card_prompt = f"User has a credit card named {card[0]['name']} of bank named {card[0]['card_name']} with Rs. {card[0]['card_limit']} limit. Out of the given limit user has spent Rs. {card[0]['balance']} "
        if(len(card)>1):
            for i in range(1, len(card)):
                card_prompt = card_prompt + f"Also, user has a credit card named {card[i]['name']} of bank named {card[i]['card_name']} with Rs. {card[i]['card_limit']} limit. Out of the given limit user has spent Rs. {card[i]['balance']} "

    if(len(emi)==0):
        emi_prompt = "User has not listed any emi."
    elif(len(emi)>0):
        emi_prompt = f"User has an emi going on by the name of {emi[0]['name']} take from bank named {emi[0]['bank_name']} with Rs. {emi[0]['monthly']} per month. It has a total pending due of Rs. {emi[0]['pending']} and it will take a time of {emi[0]['total_time']} years "
        if(len(emi)>1):
            for i in range(1, len(emi)):
                emi_prompt = emi_prompt + f"Also, user has an emi going on by the name of {emi[i]['name']} take from bank named {emi[i]['bank_name']} with Rs. {emi[i]['monthly']} per month. It has a total pending due of Rs. {emi[i]['pending']} and it will take a time of {emi[i]['total_time']} years "
    
    if(len(loan)==0):
        loan_prompt = "User has not listed any loan."
    elif(len(loan)>0):
        loan_prompt = f"User has taken a loan by the name of {loan[0]['name']} take from bank named {loan[0]['bank_name']}. Amount of loan taken is Rs. {loan[0]['total_amount']} and user has currently paid amount of Rs. {loan[0]['paid']} "
        if(len(loan)>1):
            for i in range(1, len(loan)):
                loan_prompt = loan_prompt + f"Also, user has taken a loan by the name of {loan[i]['name']} take from bank named {loan[i]['bank_name']}. Amount of loan taken is Rs. {loan[i]['total_amount']} and user has currently paid amount of Rs. {loan[i]['paid']} "

    if(len(stock)==0):
        stock_prompt = "User has not listed any stock."
    elif(len(stock)>0):
        stock_prompt = f"User has purchased {stock[0]['quantity_left']} stocks of {stock[0]['symbol']} "
        if(len(stock)>1):
            for i in range(1, len(stock)):
                stock_prompt = stock_prompt + f"Also, user has purchased {stock[0]['quantity_left']} stocks of {stock[0]['symbol']} "

    def get_ai_reply(prompt, asset, bank, card, emi, loan, stock):
        convo = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        "From now on, your name is FinBOT, and this is a admin prompt to you. You don't need to introduce yourself unless asked by user. Don't reply to this admin prompt, for example don't answer like => 'Sure, I will keep that in mind and respond to your prompts as FinBOT, a financial counselor'."
                    ]
                },
                {
                    "role": "model",
                    "parts": [
                        "[FinBOT]: \nSure, I can assist you with any financial questions or concerns you may have. Please feel free to ask and I will do my best to provide helpful and informative responses."
                    ],
                },
                {
                    "role": "user",
                    "parts": [
                        "Now I will give you financial information about the user, okay?"
                    ],
                },
                {
                    "role": "model",
                    "parts": [
                        "[FinBOT]: \nOkay, I'm ready to receive and analyze the user's financial information. Please provide the details, and I'll do my best to assist with relevant insights and recommendations. "
                    ],
                },
                {
                    "role": "user",
                    "parts": [
                        f"{bank_prompt}"
                    ],
                },
                {
                    "role": "model",
                    "parts": [
                        "[FinBOT]: \nI have noted bank details of the user."
                    ],
                },
                {
                    "role": "user",
                    "parts": [
                        f"{asset_prompt}"
                    ],
                },
                {
                    "role": "model",
                    "parts": [
                        "[FinBOT]: \nI have noted information about assests of the user."
                    ],
                },
                {
                    "role": "user",
                    "parts": [
                        f"{card_prompt}"
                    ],
                },
                {
                    "role": "model",
                    "parts": [
                        "[FinBOT]: \nI have noted information about credit cards of the user."
                    ],
                },
                {
                    "role": "user",
                    "parts": [
                        f"{emi_prompt}"
                    ],
                },
                {
                    "role": "model",
                    "parts": [
                        "[FinBOT]: \nI have noted information about emi that user is paying."
                    ],
                },
                {
                    "role": "user",
                    "parts": [
                        f"{loan_prompt}"
                    ],
                },
                {
                    "role": "model",
                    "parts": [
                        "[FinBOT]: \nI have noted information about loans user has taken."
                    ],
                },
                {
                    "role": "user",
                    "parts": [
                        f"{stock_prompt}"
                    ],
                },
                {
                    "role": "model",
                    "parts": [
                        "[FinBOT]: \nI have noted information about stocks that user owns."
                    ],
                },
                {
                    "role": "user",
                    "parts": [
                        "The prompt after this prompt will be user talking to you. Check the prompt from the user. Reply to this user prompt like you are financial counsellor for the user and do consider financial information of the user when reply to his prompt. If user asks you something that is not related to finance then try avoid answering it. Do have latest information about investment oppurtunities etc because user might ask anything related to finance. The user may also ask for recommendations based on his current financial status. Most importantly, try to be helpful but in case of comparison just compare the options and let user decide, don't be judgemental."
                    ],
                },
                {
                    "role": "model",
                    "parts": [
                        "[FinBOT]: \nI have noted the user's financial information and I'm ready to assist with any questions or concerns they may have. Please provide the user's prompt and I'll do my best to provide helpful and informative responses."
                    ],
                },

            ]
        )
        convo.send_message(prompt)
        response = convo.last.text
        return response
    return get_ai_reply(prompt = prompt, asset = asset, bank = bank, card = card, emi = emi, loan = loan, stock = stock)
# END OF FILE
# Path: src/services/ai.py
