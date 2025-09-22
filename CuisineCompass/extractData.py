import os

def merge_py_files(root_folder, output_file):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for foldername, subfolders, filenames in os.walk(root_folder):
            for filename in filenames:
                if filename.endswith('.py') and filename != os.path.basename(output_file):
                    filepath = os.path.join(foldername, filename)
                    with open(filepath, 'r', encoding='utf-8') as infile:
                        outfile.write(f"# ---- File: {filepath} ----\n")
                        outfile.write(infile.read())
                        outfile.write("\n\n")

    print(f"All .py files merged into: {output_file}")

# Example usage
merge_py_files('backend', 'merged_output.py')
