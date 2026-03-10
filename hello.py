import os
import json
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

app = FastAPI()
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


class Resources(BaseModel):
    books: list[str]
    courses: list[str]
    websites: list[str]
    youtube: list[str]
    tips: str


class ResourcesResponse(BaseModel):
    topic: str
    resources: Resources


@app.get("/resources", response_model=ResourcesResponse)
def get_resources(topic: str = Query(..., description="The topic to learn")):
    prompt = f"""You are a learning resource expert. For the topic "{topic}", return a JSON object with the best resources for someone learning from scratch.

Return ONLY a JSON object with this exact structure:
{{
  "books": ["Book Title by Author - why it's great", ...],
  "courses": ["Course Name on Platform - why it's great", ...],
  "websites": ["website.com - description", ...],
  "youtube": ["Channel/Playlist Name - description", ...],
  "tips": "Short advice paragraph for beginners starting with {topic}"
}}

Include 3-5 items per list. Be specific and practical."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )

    resources_data = json.loads(response.choices[0].message.content)
    return {"topic": topic, "resources": resources_data}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
