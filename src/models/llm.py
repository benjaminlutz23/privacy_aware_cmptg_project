import os
import logging
from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
from models.rag import vectorstore, format_docs
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def annotate_policy_section(section, llm):
    """Annotate a single section of a privacy policy using the specified language model."""
    
    retriever = vectorstore.as_retriever()

    # Define a custom prompt template
    prompt = PromptTemplate(
        input_variables=["context", "policy_section"],
        template=(
            "You are an AI agent that assigns the most appropriate privacy category icon and its corresponding color "
            "to a section of a privacy policy. Your decisions must be based on the category definitions "
            "provided in the context. Read the policy section carefully and match it to the best category. \n\n"
            "### Policy Section:\n{policy_section}\n\n"
            "### Output Format (JSON):\n"
            '{{"icon": "<associated_icon>", "color": "<color_in_english>"}}'
        )
    )

    rag_chain = (
        {"context": retriever | format_docs, "policy_section": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    result = rag_chain.invoke(section)
    return result

def print_first_three_sections(llm):
    """Read the first three sections from a specific HTML file and print the contents with annotations."""
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
        annotation = annotate_policy_section(section, llm)
        print(f"Annotation: {annotation}\n")

def run_llm_agents():
    # OpenAI
    openai_agent = ChatOpenAI(model="gpt-4", temperature=0)
    print_first_three_sections(openai_agent)

    # To do later:

    # Anthropic
    anthropic_agent = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.1, max_tokens=1000)

    # Gemini
    gemini_agent = GoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0)
