import os
import re
import json
import ast
import shutil
from ollama import chat
from ollama import ChatResponse
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.local")

LOG_ACTIVITY = os.getenv("LOG_ACTIVITY", "false").lower() == "true"

###########################################################################################################
#                                           REACT AGENT                                                   #
###########################################################################################################

REACT_TEMPLATE = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Tools input should be in JSON format.

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

IMPORTANT: You are to provide the steps until action input. Do not make up any information. The user will provide the Observation & Thought.
If the Observation statisfies the question, you should return the Final Answer.

Question: {input}
Thought:{agent_scratchpad}"""


def _parse_action(text):
    """Parse action and action input from LLM response"""
    action_pattern = r"Action:\s*(\w+)"
    input_pattern = r"Action Input:\s*(.+?)(?=\n|$)"

    # Find ALL matches
    action_matches = list(re.finditer(action_pattern, text))
    input_matches = list(re.finditer(input_pattern, text))

    # Get the LAST occurrence of each
    if action_matches and input_matches:
        last_action = action_matches[-1]  # Last action match
        last_input = input_matches[-1]  # Last input match

        action = last_action.group(1).strip()
        action_input = last_input.group(1).strip()
        return action, action_input

    return None, None


def safe_parse_json(action_input: str):
    """Safely parse action input that might be in Python dict format or JSON format"""
    try:
        # First try to parse as JSON
        return json.loads(action_input)
    except json.JSONDecodeError:
        try:
            # If JSON fails, try to parse as Python literal
            return ast.literal_eval(action_input)
        except (ValueError, SyntaxError):
            # If both fail, return empty dict
            return {}


def call_tool(action: str, action_input: dict, tools: dict):
    """Call the tool with the given action and action input"""
    if action in tools:
        tool_function = tools[action]
        # Extract the required arguments for the tool function
        tool_args = {
            k: v
            for k, v in action_input.items()
            if k in tool_function.__code__.co_varnames
        }
        return tool_function(**tool_args)
    return "Error: Tool not found"


def execute_react_agent(input: str, tools_manifest: list[str], tools: dict):

    agent_scratchpad = ""

    tools_combined = "\n".join(tools_manifest)
    tool_names = ", ".join(tool.split(":")[0].strip() for tool in tools_manifest)

    for iteration in range(10):
        prompt = REACT_TEMPLATE.format(
            tools=tools_combined,
            tool_names=tool_names,
            input=input,
            agent_scratchpad=agent_scratchpad,
        )

        if LOG_ACTIVITY:
            print("-" * 80)
            print(prompt)
            print("-" * 80)

        messages = [{"role": "user", "content": prompt}]

        try:
            response: ChatResponse = chat(
                model=os.getenv("OLLAMA_MODEL"),
                messages=messages,
                options={"temperature": 0.7, "num_ctx": 4096, "seed": 42},
            )
        except Exception as e:
            return f"Error: Failed to get response from model: {e}"

        response_content = response.message.content

        if LOG_ACTIVITY:
            print("-" * 80)
            print(f"Iteration {iteration}:")
            print(response_content)
            print("-" * 80)

        if "Final Answer:" in response_content:
            return response_content.split("Final Answer:")[1].strip()

        action, action_input = _parse_action(response_content)

        if action:
            observation = call_tool(action, safe_parse_json(action_input), tools)

            if LOG_ACTIVITY:
                print("-" * 80)
                print(f"Action: {action}")
                print(f"Action Input: {action_input}")
                print(f"Observation: {observation}")
                print("-" * 80)

            # Update scratchpad
            agent_scratchpad += (
                f" {response_content}\nObservation: {observation}\nThought:"
            )
        else:
            agent_scratchpad += f" {response_content}\nThought:"

    return "Error: Failed to get response from model"


###########################################################################################################
# VET ASSISTANT                                                                                           #
###########################################################################################################


SYSTEM_PROMPT = """
You are a helpful veterinary assistant who's goal is to answer questions about animals and their health. 
Only answer if you know the answer. If you don't know the answer, say 'I don't know'.
You are to only answer questions about animals and their health.
Always respond in a helpful and friendly manner. You do not need to mention about yourself.
"""


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
        symptoms.lower(), "Unknown symptoms. Further assessment needed."
    )
    return f"Animal Type: {animal_type}, Symptoms: {symptoms}, Assessment: {potential_conditions}"


TOOLS = {
    "get_breed_info": get_breed_info,
    "check_symptoms": check_symptoms,
}


def tools_manifest(tools: dict) -> list[str]:
    """Generates a list of tool manifests, each containing the tool name and its description.

    Args:
        tools: A dictionary where keys are tool names and values are tool descriptions.

    Returns:
        A list of strings, each representing a tool manifest in the format 'Tool Name: Tool Description'.
    """
    return [
        f"{tool_name}: {tool_description.__doc__}"
        for tool_name, tool_description in tools.items()
    ]


def run_agent(question: str) -> str:
    """Runs the agent to process a question and return a response.

    Args:
        question: The question to be processed by the agent.

    Returns:
        The content of the final response from the agent.
    """

    agent_response = execute_react_agent(question, tools_manifest(TOOLS), TOOLS)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
        {"role": "assistant", "content": agent_response.message.content},
    ]

    final_response: ChatResponse = chat(
        model=os.getenv("OLLAMA_MODEL"),
        messages=messages,
        options={"temperature": 0.7, "num_ctx": 4096, "seed": 42},
    )

    return final_response.message.content


# Can you tell me something about my dog that's a poodle?
# Why is my animal that is a dog, coughing?

# Can you tell me something about my labrador dog?
# My dog is coughing, what could be the problem?


def main():
    terminal_width = shutil.get_terminal_size().columns
    print("┌" + "─" * (terminal_width - 2) + "┐")
    print(
        "│"
        + " 🤖 Veterinary Assistant (ReAct Agent) - Interactive Chat ".center(
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

            print(
                f"Agent: {execute_react_agent(user_input, tools_manifest(TOOLS), TOOLS)}"
            )

        except KeyboardInterrupt:
            print("\n👋 Interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Please try again or type 'exit' to quit.")


if __name__ == "__main__":
    main()
