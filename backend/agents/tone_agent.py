import google.generativeai as genai
from backend.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def calibrate_tone(text:str):
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    prompt = f"""Revise the following ESG (Environmental, Social, and Governance) report to so that it meets a professional tone appropriate for government officials, corporate boards, and other relevant authorities.

The original text may contain informal phrasing, inconsistent tone and overall casual language. Your task is to:

1. Refine the tone to reflect the standards of leading consulting firms/ Big 4.
 
2. Keep the language formal, concise, and appropriate for business and policy contexts.

3. Maintain all original data and insights. Do not alter any factual information or add new content.

4. Replace informal expressions with clear and professional phrasing

5.Have proper voice like acive/passive.\nText starts here: '{text}' """
    reponse = model.generate_content(prompt)
    return reponse.text