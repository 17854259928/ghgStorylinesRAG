"""Verify that the local Ollama server and configured Qwen model respond."""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url=os.getenv("LLM_BASE_URL", "http://localhost:11434/v1"),
    api_key=os.getenv("LLM_API_KEY", "ollama"),
)

response = client.chat.completions.create(
    model=os.getenv("LLM_MODEL", "qwen3.5:9b"),
    temperature=0,
    messages=[
        {
            "role": "system",
            "content": (
                "You extract structured and verifiable information "
                "from climate-policy documents."
            ),
        },
        {
            "role": "user",
            "content": (
                "Extract the policy instrument, implementation date, "
                "target sector and mitigation objective from this text: "
                "The policy entered into force in 2024 and provides "
                "subsidies for improved manure management on EU farms. "
                "Return valid JSON."
            ),
        },
    ],
)

print(response.choices[0].message.content)
