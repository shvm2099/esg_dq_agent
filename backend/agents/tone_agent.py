import google.generativeai as genai
from backend.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def calibrate_tone(text:str):
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    prompt = f"""The objective of this task is to revise the following ESG (Environmental, Social, and Governance) report to ensure it meets the highest standards of professional communication. The revised version must align with the expectations of government agencies, corporate leadership, and regulatory bodies. The tone should reflect the formal, precise, and authoritative style characteristic of leading consulting firms such as McKinsey, PwC, Deloitte, EY, and KPMG, as well as institutional-grade reports.

The tone and style must be refined to convey professionalism and objectivity. Avoid colloquialisms, contractions, and informal phrasing. Replace casual expressions with precise, business-appropriate language. For example, phrases like "a lot of" should be changed to "a significant number of," and "we looked into" should become "an analysis was conducted." Ensure consistency in style, eliminating any abrupt shifts between casual and technical language.

The structure and language should be clear, concise, and logically organized. Prefer active voice for direct accountability, such as "The company reduced emissions," unless passive voice is necessary for neutrality or emphasis. Remove vague or subjective terms—phrases like "pretty good progress" should be revised to "notable progress," and "some improvements" should become "measurable improvements."

All factual information, including data, statistics, and key insights, must remain unchanged. The revision should enhance clarity and professionalism without altering the original meaning or introducing new content. Where claims are made, ensure they are supported by evidence to maintain credibility.

The phrasing and terminology must align with formal business and policy contexts. Replace informal descriptions with precise ESG terminology—for instance, "cut down on waste" should be revised to "implemented waste reduction initiatives," and "workers’ well-being" should be reworded as "employee welfare and occupational health."

The voice of the report must be tailored to its audience, which includes government officials, corporate boards, and regulators. For government readers, emphasize policy alignment and compliance. For corporate leadership, use strategic, performance-driven language. For regulators and investors, ensure transparency and data-backed assertions.

For example, an informal statement such as "We did pretty well on cutting emissions last year" should be revised to "The organization achieved a measurable reduction in emissions during the reporting period."

The final deliverable should be a professionally refined ESG report that retains all original data while meeting the linguistic and stylistic expectations of high-level institutional audiences. The language should convey authority, credibility, and precision, ensuring it is suitable for formal review by executives, policymakers, and regulatory bodies.
Text starts here: '{text}' """
    reponse = model.generate_content(prompt)
    return reponse.text