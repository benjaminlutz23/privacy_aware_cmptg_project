import os
import logging
import json
import re
import shutil
from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
from ai_policy_annotation.rag import extract_icon_color_options, format_context, initialize_rag_database, vectorstore, format_docs
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def get_icon_image_path(icon, color):
    """Return the image path for a given privacy icon name and color."""
    
    # Mapping of icon names to directory names
    icon_to_dir = {
        "Children Privacy": "children-privacy",
        "Data Retention": "data-retention",
        "Do Not Track": "do-not-track",
        "Expected Collection": "expected-collection",
        "Expected Use": "expected-use",
        "Heartbleed": "heartbleed",
        "Precise Location": "precise-location"
    }
    
    # Mapping of color names to file names
    color_to_file = {
        "Gray": "gray.png",
        "Green": "green.png",
        "Red": "red.png",
        "White": "white.png",
        "Yellow": "yellow.png"
    }
    
    # Ensure the provided icon and color are valid
    if icon not in icon_to_dir or color not in color_to_file:
        raise ValueError(f"Invalid icon '{icon}' or color '{color}'. Please provide a valid input.")
    
    # Construct the file path
    directory = icon_to_dir[icon]
    filename = color_to_file[color]
    image_path = f"../../privacy-icon-images/{directory}/{filename}"
    
    return image_path

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
            "### Output Format - **Return ONLY the selected icon and color in this exact format (DO NOT add extra text)**:\n\n"
            "(<chosen_icon_from_context>, <chosen_color_from_context>)"
        )
    )

    rag_chain = (
        {"context": RunnablePassthrough(), "policy_section": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    result = rag_chain.invoke({"context": structured_context, "policy_section": section}).strip()

    # Parse output like: (Precise Location, Red)
    match = re.match(r"\(([^,]+),\s*([^)]+)\)", result)
    
    if match:
        icon, color = match.groups()
        return {"icon": icon.strip(), "color": color.strip()}  # Return structured result

    logging.error(f"Invalid response format: {result}")
    return {"icon": "Unknown Icon", "color": "Unknown Color"}  # Default fallback

def save_annotations_to_json(annotations, model):
    """Save the annotations to the appropriate JSON file."""
    if model == "openai":
        json_filepath = "./src/data/llm_annotated_policies_json/openai/20_theatlantic.com.json"
    elif model == "anthropic":
        json_filepath = "./src/data/llm_annotated_policies_json/anthropic/20_theatlantic.com.json"
    elif model == "gemini":
        json_filepath = "./src/data/llm_annotated_policies_json/gemini/20_theatlantic.com.json"
    
    with open(json_filepath, "w") as json_file:
        json.dump(annotations, json_file, indent=2)
    
    logging.info(f"Annotations saved to {json_filepath}")

def annotate_and_save_sections(llm, model):
    """Read all sections from the HTML file, annotate them with icon/color pairs, and save back to the file."""

    if model == "openai":
        filepath = "./src/data/llm_annotated_policies/openai/20_theatlantic.com.html"
    elif model == "anthropic":
        filepath = "./src/data/llm_annotated_policies/anthropic/20_theatlantic.com.html"
    elif model == "gemini":
        filepath = "./src/data/llm_annotated_policies/gemini/20_theatlantic.com.html"
    
    if not os.path.exists(filepath):
        logging.error(f"File not found: {filepath}")
        return

    with open(filepath, "r") as file:
        policy_text = file.read()

    sections = policy_text.split("|||")
    updated_sections = []
    annotations = {}

    for i, section in enumerate(sections):
        try:
            # Get annotation for this section
            annotation_json = annotate_policy_section(section, llm)

            # Extract icon and color
            icon = annotation_json.get("icon", "Unknown Icon")
            color = annotation_json.get("color", "Unknown Color")
            
            # Get the image path for the icon and color
            image_path = get_icon_image_path(icon, color)
            annotation_text = f"<img src='{image_path}' alt='{icon}' style='color:{color.lower()}; padding: 5px;'><br><br>"

            # Add annotation at the end of the section
            updated_section = f"{section.rstrip()} {annotation_text}"
            updated_sections.append(updated_section)

            # Add annotation to JSON structure
            if i not in annotations:
                annotations[i] = []
            annotations[i].append({"icon": icon, "color": color})

            logging.info(f"Annotated section {i+1} with {annotation_text}")
        except Exception as e:
            logging.error(f"Error processing section {i+1}: {e}")
            updated_sections.append(section)  # Keep original section if annotation fails

    # Join sections back together and write to file
    updated_content = "|||".join(updated_sections)
    
    with open(filepath, "w") as file:
        file.write(updated_content)
    
    logging.info(f"Annotations saved to {filepath}")

    # Save annotations to JSON file
    save_annotations_to_json(annotations, model)

def run_llm_agents():
    def delete_rag_data():
        """Deletes the .rag_data directory if it exists."""
        rag_data_path = ".rag_data"
        if os.path.exists(rag_data_path) and os.path.isdir(rag_data_path):
            shutil.rmtree(rag_data_path)
            logging.info(f"Deleted directory: {rag_data_path}")

    # OpenAI
    model = "openai"
    openai_agent = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    # delete_rag_data()
    # initialize_rag_database()
    # annotate_and_save_sections(openai_agent, model)


    # Anthropic
    model = "anthropic"
    anthropic_agent = ChatAnthropic(model="claude-3-5-sonnet-latest", temperature=0)
    # delete_rag_data()
    # initialize_rag_database()
    # annotate_and_save_sections(anthropic_agent, model)

    # Gemini
    model = "gemini"
    gemini_agent = GoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0)
    delete_rag_data()
    initialize_rag_database()
    annotate_and_save_sections(gemini_agent, model)
