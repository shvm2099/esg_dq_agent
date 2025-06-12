import google.generativeai as genai
from backend.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def validate_structure(text: str, suggestions:str):
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    prompt = f"""

You are tasked with professionally restructuring the provided ESG (Environmental, Social, and Governance) report to meet the highest standards typical of the Big 4 consulting and auditing firms, ensuring it is suitable for review by government authorities, board members, and executive stakeholders.

Your objectives are:
Organize the entire report strictly under the following formal sections:
Executive Summary
Organizational Profile
Stakeholder Engagement
Material Topics
Management Approach
Environmental Performance
Social Performance
Governance
Conclusions and Future Outlook

Appendices (if applicable), reserved for supplementary data, charts, or technical notes.

Within each section, arrange the content into coherent, complete paragraphs that communicate ideas clearly, concisely, and logically—avoid bullet points, fragmented statements, or overly brief lines.
Ensure each paragraph transitions smoothly to the next, preserving a logical narrative flow that guides the reader effortlessly through the content.
Use formal, precise headers and subheaders as needed to improve clarity, but only insert them when they add meaningful structure.
Remove redundant or misplaced headers and content, consolidating information appropriately without altering the factual accuracy or the professional, objective tone of the original text.
Preserve the original wording and tone as much as possible, refraining from rewriting the content except to enhance paragraph structure and flow.
Where content overlaps or repeats, merge it into comprehensive paragraphs within the most relevant section, ensuring clarity and avoiding unnecessary repetition.
Clearly mark the Appendices section, and limit its contents to supplementary materials such as detailed data tables, charts, or methodological notes.
Ensure the final document reads as a polished, authoritative, and formal ESG report, embodying best practices in corporate disclosure and regulatory compliance.

some suggestions for headers and subheaders :\n{suggestions}\n
ESG Report to be reconstruct:
{text}"""
    
    response = model.generate_content(prompt)
    return response.text
