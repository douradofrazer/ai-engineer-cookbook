import os
import shutil
from ollama import chat
from ollama import ChatResponse
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """
You are a helpful veterinary assistant who's goal is to answer questions about animals and their health. 
Only answer if you know the answer. If you don't know the answer, say 'I don't know'.
You are to only answer questions about animals and their health.
Always respond in a helpful and friendly manner. You do not need to mention about yourself.
"""


def call_llm(question: str) -> None:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]
    response: ChatResponse = chat(
        model=os.getenv("OLLAMA_MODEL"),
        messages=messages,
        options={"temperature": 0.7, "num_ctx": 1024, "seed": 42},
    )
    print("LLM:", response.message.content)


def call_llm_streaming(question: str) -> None:
    """Stream the LLM response to terminal in real-time."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]

    print("LLM: ", end="", flush=True)

    for chunk in chat(
        model="gemma3:4b",
        messages=messages,
        options={"temperature": 0.7, "num_ctx": 1024, "seed": 42},
        stream=True,
    ):
        if chunk.message.content:
            print(chunk.message.content, end="", flush=True)
    print()


def main():
    terminal_width = shutil.get_terminal_size().columns
    print("┌" + "─" * (terminal_width - 2) + "┐")
    print(
        "│"
        + " 🤖 Veterinary Assistant (Simple LLM Calling) - Interactive Chat ".center(
            terminal_width - 3
        )
        + "│"
    )
    print(
        "│"
        + " Ask me anything about animal health and veterinary care! ".center(
            terminal_width - 2
        )
        + "│"
    )
    print("│" + " Type 'exit' to quit ".center(terminal_width - 2) + "│")
    print("└" + "─" * (terminal_width - 2) + "┘")
    print()

    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() in ("exit", "quit"):
                print("Goodbye! Take care of your furry friends!")
                break

            if not user_input:
                continue

            call_llm_streaming(user_input)

        except KeyboardInterrupt:
            print("\n👋 Interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Please try again or type 'exit' to quit.")


if __name__ == "__main__":
    main()
