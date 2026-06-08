import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def get_health_remarks(name: str, age: int, glucose: float, haemoglobin: float, cholesterol: float) -> str:
    if not GEMINI_API_KEY:
        return "Configuration error: GEMINI_API_KEY is not set in your .env file."

    prompt = build_health_prompt(name, age, glucose, haemoglobin, cholesterol)

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception:
        return "AI service configuration failed. Please check your API setup."

    max_retries = 3
    delay = 2

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            if response and getattr(response, "text", None):
                return response.text.strip()

            return "AI prediction is temporarily unavailable. Record saved successfully."

        except Exception as e:
            error_msg = str(e).lower()

            if "quota" in error_msg or "429" in error_msg or "exhausted" in error_msg:
                return "API quota reached. Please try again later or use another API key."

            if "api key" in error_msg or "invalid" in error_msg or "401" in error_msg:
                return "Invalid API key. Please check your GEMINI_API_KEY in the .env file."

            if "network" in error_msg or "connect" in error_msg or "connection" in error_msg:
                if attempt < max_retries - 1:
                    time.sleep(delay)
                    delay *= 2
                    continue
                return "Network error. Please check your internet connection and try again."

            if "503" in error_msg or "unavailable" in error_msg or "overloaded" in error_msg or "high demand" in error_msg:
                if attempt < max_retries - 1:
                    time.sleep(delay)
                    delay *= 2
                    continue
                return "AI prediction is temporarily unavailable due to high demand. Record saved successfully."

            if attempt < max_retries - 1:
                time.sleep(delay)
                delay *= 2
                continue

            return "Health prediction is temporarily unavailable. Record saved successfully."


def build_health_prompt(name: str, age: int, glucose: float, haemoglobin: float, cholesterol: float) -> str:
    prompt = f"""You are a medical AI assistant helping to flag potential health risks based on blood test results.

Patient Information:
- Name: {name}
- Age: {age} years old
- Glucose level: {glucose} mg/dL
- Haemoglobin level: {haemoglobin} g/dL
- Cholesterol level: {cholesterol} mg/dL

Based on these blood test values, provide a brief health assessment:
1. Mention if any values are outside the normal reference range
2. Suggest possible health conditions or risks associated with these values
3. Recommend whether the patient should consult a doctor

Normal reference ranges:
- Glucose (fasting): 70-99 mg/dL (pre-diabetic: 100-125, diabetic: 126+)
- Haemoglobin: Men 13.5-17.5 g/dL, Women 12.0-15.5 g/dL
- Total Cholesterol: below 200 mg/dL (borderline: 200-239, high: 240+)

Keep your response concise - 3 to 4 sentences maximum. Do not include disclaimers about not being a real doctor."""
    return prompt