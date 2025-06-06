import google.generativeai as genai
from backend.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def validate_structure(text: str):
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    prompt = f"""

Restructure the following ESG (Environmental, Social, and Governance) report to ensure it follows a clear, formal section hierarchy in line with professional standards used by major consulting firms/big 4.

This report may be reviewed by government authorities, board members, and executive stakeholders, so it must be upto that standard

Use following sectional framework if possible/applicable:
1.Executive Summary
2. Context and Objectives
3. Methodology, Data sources, ESG framework
4. ESG performance Analysis and key Findings
5. Risks, challanges, Opportunities
6. Conclusions and (if applicable) Recommendations
Appendices (if applicable)Supplementary data, charts, or technical notes

Your task is to:
Organize the text under appropriate sections and each scetion has clarity
Ensure there is logical flow
Remove redundant headers or misplaced content
Add headers, titles, subtitles where necessary
Do not alter factual content or tone (leave wording/tone intact where possible)
Insert or adjust headers/subheaders only as needed for structure

Input ESG Report:
{text}"""
    
    response = model.generate_content(prompt)
    return response.text
