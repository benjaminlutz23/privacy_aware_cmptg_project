# Privacy-Aware Computing Project

## Abstract
This project aims to improve privacy policy comprehension by leveraging Large Language Models (LLMs) to assign structured privacy icons to sections of privacy policies.

## Project Goals
- Evaluate ChatGPT-4o, Claude 3.5 Sonnet, and Gemini 2.0 Flash in assigning privacy icons to policy sections.
- Develop a benchmark dataset for evaluating accuracy.
- Build a web-based tool to demonstrate privacy icon assignments in real-time.

## Project Structure
- `src/`: Source code directory.
  - `app.py`: Main Flask application.
  - `controllers/`: Directory for controller-related code.
  - `models/`: Directory for model-related code.
  - `utils/`: Utility functions.
  - `static/`: Static files (CSS, JS, images).
  - `templates/`: HTML templates for the web application.

## Setup Instructions
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run the Flask application: `python src/app.py`.
