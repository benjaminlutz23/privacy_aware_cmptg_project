import json
import matplotlib.pyplot as plt
import os

# Load JSON data
def load_json(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

# Compare JSON data
def compare_policies(gemini, benchmark):
    total_match = 0
    total_no_match = 0
    for key in gemini.keys():
        gemini_set = set((item['icon'], item['color']) for item in gemini[key])
        benchmark_set = set((item['icon'], item['color']) for item in benchmark.get(key, []))
        total_match += len(gemini_set & benchmark_set)
        total_no_match += len(gemini_set - benchmark_set)
    return total_match, total_no_match

# Print summary statistics
def print_summary(total_match, total_no_match):
    total_items = total_match + total_no_match
    print(f"Total Matches: {total_match}")
    print(f"Total Items: {total_items}")
    print(f"Match Percentage: {total_match / total_items * 100:.2f}%")

# Plot comparison
def plot_comparison(total_match, total_no_match, title):
    labels = ['Match', 'No Match']
    sizes = [total_match, total_no_match]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    plt.title(title)
    plt.show()

# Main function
def main():
    gemini_dir = './src/data/llm_annotated_policies_json/gemini'
    openai_dir = './src/data/llm_annotated_policies_json/openai'
    benchmark_dir = './src/data/benchmark/benchmarked_policies'

    total_match_gemini = 0
    total_no_match_gemini = 0
    total_match_openai = 0
    total_no_match_openai = 0

    for filename in os.listdir(gemini_dir):
        gemini_path = os.path.join(gemini_dir, filename)
        benchmark_path = os.path.join(benchmark_dir, filename)

        if os.path.exists(benchmark_path):
            gemini = load_json(gemini_path)
            benchmark = load_json(benchmark_path)

            match, no_match = compare_policies(gemini, benchmark)
            total_match_gemini += match
            total_no_match_gemini += no_match

    for filename in os.listdir(openai_dir):
        openai_path = os.path.join(openai_dir, filename)
        benchmark_path = os.path.join(benchmark_dir, filename)

        if os.path.exists(benchmark_path):
            openai = load_json(openai_path)
            benchmark = load_json(benchmark_path)

            match, no_match = compare_policies(openai, benchmark)
            total_match_openai += match
            total_no_match_openai += no_match

    print("Gemini Comparison:")
    print_summary(total_match_gemini, total_no_match_gemini)
    plot_comparison(total_match_gemini, total_no_match_gemini, 'Gemini Overall Comparison')

    print("OpenAI Comparison:")
    print_summary(total_match_openai, total_no_match_openai)
    plot_comparison(total_match_openai, total_no_match_openai, 'OpenAI Overall Comparison')

if __name__ == "__main__":
    main()
