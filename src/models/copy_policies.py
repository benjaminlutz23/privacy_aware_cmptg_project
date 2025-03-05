import os
import shutil

def copy_files(src_dir, dest_dirs):
    if not os.path.exists(src_dir):
        raise FileNotFoundError(f"Source directory {src_dir} does not exist")

    for dest_dir in dest_dirs:
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        for filename in os.listdir(src_dir):
            src_file = os.path.join(src_dir, filename)
            dest_file = os.path.join(dest_dir, filename)
            shutil.copy2(src_file, dest_file)

def main():
    src_dir = '../src/data/opp-115-dataset/sanitized_policies'
    dest_dirs = [
        '../src/data/llm_annotated_policies/openai',
        '../src/data/llm_annotated_policies/anthropic',
        '../src/data/llm_annotated_policies/gemini'
    ]
    copy_files(src_dir, dest_dirs)

if __name__ == '__main__':
    main()
