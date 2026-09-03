from app.services.gemini_service import ask_gemini

response = ask_gemini("Say hello in one short sentence.")

print(response)