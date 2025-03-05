import os
from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAI
from langchain_anthropic import ChatAnthropic

def get_image_paths(directory):
    image_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.png'):
                image_paths.append(os.path.join(root, file))
    return image_paths

def create_html_file(llm_name, image_paths):
    html_content = "<html><body><h1>Hello World from {}</h1>".format(llm_name)
    for image_path in image_paths:
        image_name = os.path.basename(image_path)
        html_content += '<div><img src="{}" alt="{}"><p>{}</p></div>'.format(image_path, image_name, image_name)
    html_content += "</body></html>"

    output_dir = '../data/llm_annotated_policies'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_path = os.path.join(output_dir, '{}_icon_assignment.html'.format(llm_name))
    with open(output_path, 'w') as file:
        file.write(html_content)

def run_llm_agents():
    image_paths = get_image_paths('../privacy-icon-images')

    # OpenAI
    openai_agent = ChatOpenAI(model="gpt-4", temperature=0)
    create_html_file('openai', image_paths)

    # Anthropic
    anthropic_agent = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.1, max_tokens=1000)
    create_html_file('anthropic', image_paths)

    # Gemini
    gemini_agent = GoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0)
    create_html_file('gemini', image_paths)

# Placeholder for LLM interaction code
def assign_privacy_icons(policy_text):
    run_llm_agents()
    return {"icons": []}
