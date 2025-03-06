import os
import json
import logging
import time
from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAI
from langchain_anthropic import ChatAnthropic

def print_first_three_sections():
    """ Read the first three sections from a specific HTML file and print the contents to stdout. """
    filepath = "./src/data/llm_annotated_policies/openai/20_theatlantic.com.html"
    
    if not os.path.exists(filepath):
        logging.error(f"File not found: {filepath}")
        return

    with open(filepath, "r") as file:
        policy_text = file.read()

    sections = policy_text.split("|||")
    first_three_sections = sections[:3]

    for i, section in enumerate(first_three_sections):
        print(f"Section {i+1}:\n{section}\n")

def run_llm_agents():
    # OpenAI
    openai_agent = ChatOpenAI(model="gpt-4", temperature=0)

    # To do later:

    # Anthropic
    anthropic_agent = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.1, max_tokens=1000)

    # Gemini
    gemini_agent = GoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0)
