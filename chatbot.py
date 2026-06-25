"Project 1"

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL_NAME = "gemini-2.0-flash"
EXIT_COMMANDS = {"exit", "quit", "disconnect"}

SYSTEM_PROMPT = """
You are a friendly, natural-sounding AI assistant for DecodeLabs.
Keep replies short, conversational, and useful.
If the user sounds casual, reply casually.
If the user asks for code or technical help, explain it clearly with small examples.
Do not pretend to know private project details unless the user provides them.
""".strip()


def build_rules():
    greeting = "Bot: Hey! I am online. Ask me anything, or type 'help' for commands."

    return {
        "hello"   : greeting,
        "hi"      : greeting,
        "hey"     : greeting,
        "status"  : "Bot: STATUS: Operational | Rule layer active | LLM fallback ready.",
        "help"    : "Bot: Commands: 'hello', 'status', 'system 1', 'system 2', 'clear', 'exit'.",
        "system 1": "Bot: System 1 is the LLM layer: flexible, creative, and natural.",
        "system 2": "Bot: System 2 is the rule layer: predictable guardrails and exact commands.",
    }


def create_chat_session():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Missing GEMINI_API_KEY. Set it first, then run the chatbot again."
        )

    client = genai.Client(api_key=api_key)
    return client


def get_llm_response(client, chat_history, user_input):
    chat_history.append(user_input)

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=chat_history,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            max_output_tokens=300,
        )
    )

    reply = response.text.strip()
    chat_history.append(reply)
    return reply


def run_chatbot():
    print("=" * 58)
    print("   DECODELABS HYBRID LOGIC ENGINE v3.0")
    print("   Rule-Based Guardrails + Gemini LLM Active")
    print("   Type 'exit' to disconnect.")
    print("=" * 58)

    try:
        client = create_chat_session()
    except RuntimeError as error:
        print(f"Bot: {error}")
        return

    responses = build_rules()
    chat_history = []

    while True:
        try:
            raw_input = input("You: ").strip()
            user_input = raw_input.lower()

            if not user_input:
                print("Bot: I didn't catch that. Go ahead!")
                continue

            if user_input in EXIT_COMMANDS:
                print("\nBot: Session closed. See you, engineer!")
                print("=" * 58)
                break

            if user_input == "clear":
                chat_history = []
                print("Bot: Chat memory cleared.")
                continue

            if user_input in responses:
                print(responses[user_input])
                continue

            reply = get_llm_response(client, chat_history, raw_input)
            print("Bot:", reply)

        except (KeyboardInterrupt, EOFError):
            print("\n\nBot: Interruption detected. Clean exit complete.")
            break
        except Exception as error:
            print("Bot: Something went wrong on my end. Try again!")


if __name__ == "__main__":
    run_chatbot()