from services import get_services


services = get_services()

async def generate_mcq(text: str):
    prompt = f"""
You are a quiz generator. Create ONLY multiple-choice questions 
from the text below.

Text:
{text}

Generate exactly 5 MCQs with:
- question
- 4 options (A, B, C, D)
- correct answer letter

Output ONLY valid JSON, in this exact format:

{{
  "mcq": [
    {{
      "question": "...",
      "options": ["A...", "B...", "C...", "D..."],
      "answer": "A"
    }}
  ]
}}
"""

    raw = services["call_ai"](prompt)
    cleaned = services["extract_json"](raw)

    return {"quiz": cleaned}
