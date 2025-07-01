import os
import json
import shutil
from ollama import chat
from ollama import ChatResponse
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.local")

LOG_ACTIVITY = os.getenv("LOG_ACTIVITY", "false").lower() == "true"


def get_breed_info(breed: str, animal_type: str) -> str:
    """Retrieves breed-specific health information, common conditions, and care requirements.

    Args:
        breed: The breed of the animal for which information is requested.
        animal_type: The type of animal (e.g., 'dog', 'cat').

    Returns:
        A string containing health information, common conditions, and care requirements for the specified breed.
        If the breed or animal type is not found, returns a default message with the breed and animal type.
    """
    mock_data = {
        "dog": {
            "labrador": "Labradors are prone to hip dysplasia and obesity. Regular exercise and a balanced diet are essential.",
            "poodle": "Poodles often face eye disorders and skin allergies. Regular grooming and vet check-ups are recommended.",
        },
        "cat": {
            "siamese": "Siamese cats can have respiratory issues and dental problems. Regular dental care and a smoke-free environment are beneficial.",
            "maine coon": "Maine Coons are susceptible to heart disease and hip dysplasia. Regular vet visits and a healthy diet are important.",
        },
    }

    return mock_data.get(animal_type.lower(), {}).get(
        breed.lower(), f"Breed: {breed}, Animal Type: {animal_type}"
    )


def check_symptoms(animal_type: str, symptoms: str) -> str:
    """Analyzes symptoms and provides an initial assessment for animals.

    Args:
        animal_type: The type of animal (e.g., 'dog', 'cat').
        symptoms: A description of the symptoms observed in the animal.

    Returns:
        A string containing an assessment of the symptoms, including potential conditions and urgency.
        If the symptoms or animal type are not recognized, returns a message indicating that further assessment is needed.
    """
    mock_symptom_data = {
        "dog": {
            "coughing": "Coughing in dogs can indicate kennel cough or heart disease. Urgency: Moderate.",
            "vomiting": "Vomiting may be due to dietary indiscretion or gastrointestinal issues. Urgency: High if persistent.",
        },
        "cat": {
            "sneezing": "Sneezing in cats can be a sign of upper respiratory infection. Urgency: Moderate.",
            "lethargy": "Lethargy might indicate anemia or infection. Urgency: High if accompanied by other symptoms.",
        },
    }

    potential_conditions = mock_symptom_data.get(animal_type.lower(), {}).get(
        symptoms, "Unknown symptoms. Further assessment needed."
    )
    return f"Animal Type: {animal_type}, Symptoms: {symptoms}, Assessment: {potential_conditions}"


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_breed_info",
            "description": "Get the breed information for a given animal type and breed.",
            "parameters": {
                "type": "object",
                "properties": {
                    "animal_type": {
                        "type": "string",
                        "description": "The type of animal (e.g., dog, cat)",
                    },
                    "breed": {
                        "type": "string",
                        "description": "The breed of the animal",
                    },
                },
                "required": ["animal_type", "breed"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_symptoms",
            "description": "Check the symptoms of an animal.",
            "parameters": {
                "type": "object",
                "properties": {
                    "animal_type": {
                        "type": "string",
                        "description": "The type of animal (e.g., 'dog', 'cat')",
                    },
                    "symptoms": {
                        "type": "string",
                        "description": "The symptoms of the animal",
                    },
                },
                "required": ["animal_type", "symptoms"],
            },
        },
    },
]

SYSTEM_PROMPT = """
You are a helpful veterinary assistant who's goal is to answer questions about animals and their health. 
Only answer if you know the answer. If you don't know the answer, say 'I don't know'.
You are to only answer questions about animals and their health.
Always respond in a helpful and friendly manner. You do not need to mention about yourself.
"""


def call_tool(func_name: str, args: dict) -> str:

    if LOG_ACTIVITY:
        print("-" * 100)
        print(f"Tool: {func_name}")
        print(f"Arguments: {args}")
        print("-" * 100)

    if func_name == "get_breed_info":
        return get_breed_info(args["breed"], args["animal_type"])
    elif func_name == "check_symptoms":
        return check_symptoms(args["animal_type"], args["symptoms"])


def call_llm(question: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]

    response: ChatResponse = chat(
        model=os.getenv("OLLAMA_TOOL_CALLING_MODEL"),
        messages=messages,
        options={"temperature": 0.7, "num_ctx": 4096, "seed": 42},
        tools=TOOLS,
    )

    try:
        # Check if tool call was made
        tool_calls = response["message"]["tool_calls"]

        if LOG_ACTIVITY:
            print("-" * 100)
            print(f"Tool Calls: {tool_calls}")
            print("-" * 100)

        if tool_calls:
            for tool_call in tool_calls:
                func_name = tool_call["function"]["name"]
                args = tool_call["function"]["arguments"]

            result = call_tool(func_name, args)

            if LOG_ACTIVITY:
                print("-" * 100)
                print(f"Result: {result}")
                print("-" * 100)

            # Feed tool output back
            messages.append(
                {"role": "assistant", "tool_called": func_name, "content": None}
            )
            messages.append(
                {"role": "tool", "tool_called": func_name, "content": result}
            )

        if LOG_ACTIVITY:
            print("-" * 100)
            print(f"Messages: {messages}")
            print("-" * 100)

        final: ChatResponse = chat(
            model=os.getenv("OLLAMA_TOOL_CALLING_MODEL"),
            messages=messages,
            options={"temperature": 0.7, "num_ctx": 4096, "seed": 42},
        )

        return final.message.content

    except Exception as e:
        return response.message.content


def main():
    terminal_width = shutil.get_terminal_size().columns
    print("┌" + "─" * (terminal_width - 2) + "┐")
    print(
        "│"
        + " 🤖 Veterinary Assistant (Tool Calling) - Interactive Chat ".center(
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

            print(call_llm(user_input))

        except KeyboardInterrupt:
            print("\n👋 Interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Please try again or type 'exit' to quit.")


# Can you tell me something about my dog that's a labrador?
# My dog is coughing, what could be the problem?

if __name__ == "__main__":
    main()
