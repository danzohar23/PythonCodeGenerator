import openai
import subprocess
import random
import platform

# Set your OpenAI API key here
api_key = "YOUR_API_KEY_HERE"

# Initialize the OpenAI API client
openai.api_key = api_key

# List of available programs
PROGRAMS_LIST = [
    """Given two strings str1 and str2, prints all interleavings of the given two strings. You may assume that all characters in both strings are different. Input: str1 = "AB", str2 = "CD" Output: ABCD ACBD ACDB CABD CADB CDAB Input: str1 = "AB", str2 = "C" Output: ABC ACB CAB """,
    "A program that checks if a number is a palindrome",
    "A program that finds the kth smallest element in a given binary search tree.",
    "A program that generates the Fibonacci sequence up to a certain number or till a certain number of elements.",
    "A program that implements dijkstra's algorithm",
]


def get_random_program():
    return random.choice(PROGRAMS_LIST)


conversation_history = []


def chat_with_gpt(prompt, conversation_history):
    try:
        messages = [{"role": "user", "content": prompt}]
        for previous_message in conversation_history:
            role = "system" if previous_message.startswith("ChatGPT:") else "user"
            messages.append({"role": role, "content": previous_message})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
            max_tokens=1000,
        )
        latest_response = response.choices[0].message["content"].strip()
        return latest_response
    except Exception as e:
        return str(e)


# Function to write the response to a file
def write_to_file(response_text):
    try:
        with open("generatedcode.py", "w") as file:
            file.write(response_text)
        print("Response saved to generatedfile.py")
    except Exception as e:
        print(f"Error writing to file: {e}")


# Function to clear the generatedcode.py file
def clear_generated_file():
    with open("generatedcode.py", "w") as file:
        file.write("")


# Function to open the generatedcode.py file
def open_generated_code_file():
    if platform.system() == "Windows":
        subprocess.Popen(["start", "generatedcode.py"], shell=True)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", "generatedcode.py"])
    else:
        subprocess.Popen(["xdg-open", "generatedcode.py"])


# Main function to chat with GPT
def main():
    clear_generated_file()
    print(
        "Welcome to The Super Python Coder! Tell me, which program would you like me to code for you? If you don't have an idea,just press enter and I will choose a random program to code"
    )
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        if user_input.strip() == "":
            # If the user pressed Enter, choose a random program
            user_input = get_random_program()

        full_prompt = (
            "You are an expert python developer. Create the following program without any formatting:\n"
            + user_input
            + """\n.Remember to include 5 unit tests written in python below the code to check the logic of the program using 5 different inputs and expected outputs. DO NOT include any formatting like "```python". DO NOT include comments or explanations, just the plain code."""
        )
        response = chat_with_gpt(full_prompt, conversation_history)
        conversation_history.append(response)
        print("ChatGPT:", response)
        # Write the response to a file
        write_to_file(response)
        try:
            result = subprocess.run(
                ["python", "generatedcode.py"],
                capture_output=True,
                text=True,
                check=True,
            )
            print(result.stdout)
            print("Code creation completed successfully!")
            open_generated_code_file()
            break
        except subprocess.CalledProcessError as e:
            print("Error generating code! {" + e.stderr + "}")

        i = 1
        for i in range(5):
            try:
                result = subprocess.run(
                    ["python", "generatedcode.py"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                print(result.stdout)
                print("Code creation completed successfully!")
                open_generated_code_file()
                return
            except subprocess.CalledProcessError as e:
                print("Error generating code! {" + e.stderr + "}")
                clear_generated_file()
                i = i + 1
                if i == 4:
                    print("Code generation failed!")
                    return
                full_prompt = (
                    "I have recieved the following error:\n"
                    + e.stderr
                    + ".\nCan you please write the corrected code with no formatting from your last answer after analysing the error message? Remember to only write code with no formatting or explanations. Also include 5 unit tests."
                )
                response = chat_with_gpt(full_prompt, conversation_history)
                conversation_history.append(response)
                print("ChatGPT:", response)
                write_to_file(response)


if __name__ == "__main__":
    main()
