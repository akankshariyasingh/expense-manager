import os
import time

from dotenv import load_dotenv
from google import genai


load_dotenv()


api_key = os.getenv("GEMINI_API_KEY")

print("Gemini API key loaded:", bool(api_key))


client = genai.Client(
    api_key=api_key
)


def ask_gemini(prompt: str) -> str:

    start_time = time.time()

    try:

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        elapsed_time = time.time() - start_time

        print(
            f"Gemini response time: "
            f"{elapsed_time:.2f} seconds"
        )

        return response.text

    except Exception as e:

        elapsed_time = time.time() - start_time

        print(
            f"Gemini error after "
            f"{elapsed_time:.2f} seconds: {e}"
        )

        error_message = str(e)

        if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:

            return (
                "The AI assistant has temporarily reached "
                "its usage limit. Please try again later."
            )

        return (
            "The AI assistant is temporarily unavailable. "
            "Please try again later."
        )