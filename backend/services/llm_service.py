import os
from google import genai
from google.genai import types
from utils.parser import parse_json

# Keep these braces as they are (no doubling needed with this method)
PROMPT_TEMPLATE = """
You are an expert interview evaluator.

Evaluate the following candidate response based on:
1. Clarity
2. Structure
3. Technical Depth
4. Relevance
5. Communication

Response:
{response}

Return ONLY JSON like this:
{
  "clarity_score": 1,
  "structure_score": 1,
  "depth_score": 1,
  "relevance_score": 1,
  "communication_score": 1
}
"""

def build_prompt(response: str) -> str:
    # This replaces the literal '{response}' text with your input string
    return PROMPT_TEMPLATE.replace("{response}", response)

def call_llm(client, prompt: str):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction="You are a strict evaluator.",
            temperature=0.2,
        )
    )
    return response.text

def evaluate_response(response: str):
    # Initialize the client
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    # Generate the prompt
    prompt = build_prompt(response)
    
    # Get LLM output
    raw_output = call_llm(client, prompt)
    
    # Parse and return
    return parse_json(raw_output)