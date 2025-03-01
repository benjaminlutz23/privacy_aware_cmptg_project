# Privacy-Aware Computing Project

## Abstract
This project aims to improve privacy policy comprehension by leveraging Large Language Models (LLMs) to assign structured privacy icons to sections of privacy policies.

## Project Goals
- Evaluate ChatGPT-4o, Claude 3.5 Sonnet, and Gemini 2.0 Flash in assigning privacy icons to policy sections.
- Develop a benchmark dataset for evaluating accuracy.
- Build a web-based tool to demonstrate privacy icon assignments in real-time.

## Benchmark creation

### Dataset

The OPP-115 dataset contains 115 privacy policies which were annotated by several law school students. Since multiple people annotated the same policies, there are naturally some conflicts in the annotations. 

As such, the corpus provides consoldated datasets at differnt thresholds.  Consolidation is the process of retaining valuable annotations while reducing redundancy, and a threshold in the consolidation process determines how strictly data practices from different annotators are merged into a single annotation. Datasets for three threshold values were provided:

- Threshold = 1 → Strictest merging: Only data practices that all annotators agree on (i.e., fully overlapping annotations) are consolidated. This results in the most conservative dataset, keeping only high-confidence annotations.

-	Threshold = 0.75 → Moderate merging: Data practices with significant but not complete overlap across annotators are consolidated. Some disagreements are tolerated, but there is still a strong emphasis on agreement.

-	Threshold = 0.5 → Lenient merging: Data practices with partial overlap are consolidated, even if annotators did not fully agree on the exact text spans. This results in a larger dataset with more diverse annotations but may include less precise labeling.

For our purposes, we wanted only the highest-confidence annotations, which are the ones that all the annotators agree on. Thus our benchmark uses the OPP-115 dataset with a threshold of 1, and datasets corresponding to other threshold values are ignored.

## Setup Instructions
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run the Flask application: `python src/app.py`.
