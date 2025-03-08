import os
import logging
import json
from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
from ai_policy_annotation.rag import extract_icon_color_options, format_context, vectorstore, format_docs
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def annotate_policy_section(section, llm):
    """Annotate a single section of a privacy policy using the LLM with properly structured context."""
    
    retriever = vectorstore.as_retriever()
    retrieved_docs = retriever.invoke(section)  # Fetch relevant category JSON
    retrieved_context = format_docs(retrieved_docs)  # Convert to string

    # Extract and format only valid (icon, color) pairs
    icon_color_pairs = extract_icon_color_options(retrieved_docs)
    structured_context = format_context(icon_color_pairs)

    prompt = PromptTemplate(
        input_variables=["context", "policy_section"],
        template=(
            "You are an AI tasked with assigning the most appropriate **privacy category icon and its corresponding color** "
            "to a section of a privacy policy. \n\n"
            "**Use ONLY the provided icons and colors from the structured list below. Do NOT generate new icons or colors.**\n\n"
            "### Available Icons and Colors:\n{context}\n\n"
            "### Policy Section:\n{policy_section}\n\n"
            "### Output Format (JSON) - **Strictly choose an icon/color from the list**:\n"
            '{{"icon": "<chosen_icon_from_context>", "color": "<chosen_color_from_context>"}}'
        )
    )

    rag_chain = (
        {"context": RunnablePassthrough(), "policy_section": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    result = rag_chain.invoke({"context": structured_context, "policy_section": section})
    return result

def annotate_and_save_sections(llm):
    """Read all sections from the HTML file, annotate them with icon/color pairs, and save back to the file."""
    filepath = "./src/data/llm_annotated_policies/openai/20_theatlantic.com.html"
    
    if not os.path.exists(filepath):
        logging.error(f"File not found: {filepath}")
        return

    with open(filepath, "r") as file:
        policy_text = file.read()

    sections = policy_text.split("|||")
    updated_sections = []

    for i, section in enumerate(sections):
        try:
            # Get annotation for this section
            annotation_str = annotate_policy_section(section, llm)
            
            # Try to parse the JSON to extract icon and color
            try:
                annotation_json = json.loads(annotation_str)
                icon = annotation_json.get("icon", "Unknown Icon")
                color = annotation_json.get("color", "Unknown Color")
                annotation_text = f"<span style='color:{color.lower()};'>[{icon}]</span>"
            except json.JSONDecodeError:
                logging.error(f"Failed to parse annotation JSON: {annotation_str}")
                annotation_text = "[Annotation Error]"
            
            # Add annotation at the end of the section
            updated_section = f"{section.rstrip()} {annotation_text}"
            updated_sections.append(updated_section)
            
            logging.info(f"Annotated section {i+1} with {annotation_text}")
        except Exception as e:
            logging.error(f"Error processing section {i+1}: {e}")
            updated_sections.append(section)  # Keep original section if annotation fails

    # Join sections back together and write to file
    updated_content = "|||".join(updated_sections)
    
    with open(filepath, "w") as file:
        file.write(updated_content)
    
    logging.info(f"Annotations saved to {filepath}")

def run_llm_agents():
    # OpenAI
    openai_agent = ChatOpenAI(model="gpt-4", temperature=0)
    annotate_and_save_sections(openai_agent)

    # To do later:

    # Anthropic
    anthropic_agent = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.1, max_tokens=1000)

    # Gemini
    gemini_agent = GoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0)
