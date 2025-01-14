# generate_html_pages

# generate_html_pages.py Version 0.1 by chatGPT-4o

"""
This script generates static HTML pages for visualization based on metadata CSV files stored in './output_metadata'.

Usage:
1. Place metadata files in './output_metadata'.
2. Ensure templates for each page are in './templates'.
3. Run the script. It will create the './output_pages' directory if it does not exist.
4. The generated HTML pages will be saved in './output_pages'.

Required Input Files:
- 1_standardized-core-metrics-populated.csv
- 2_standardized-groupcode-metrics-populated.csv
- 3_standardized-course-rankings-populated.csv
- 4_standardized-size-distribution-populated.csv
- 5_standardized-detailed-stats-populated.csv

"""

import os
import pandas as pd
from jinja2 import Environment, FileSystemLoader

# Directories
metadata_dir = './output_metadata'
output_pages_dir = './output_pages'

# Ensure the output pages directory exists
os.makedirs(output_pages_dir, exist_ok=True)

# Input metadata files
metadata_files = {
    "core_metrics": os.path.join(metadata_dir, "1_standardized-core-metrics-populated.csv"),
    "groupcode_metrics": os.path.join(metadata_dir, "2_standardized-groupcode-metrics-populated.csv"),
    "course_rankings": os.path.join(metadata_dir, "3_standardized-course-rankings-populated.csv"),
    "size_distribution": os.path.join(metadata_dir, "4_standardized-size-distribution-populated.csv"),
    "detailed_stats": os.path.join(metadata_dir, "5_standardized-detailed-stats-populated.csv")
}

# Load metadata files into dataframes
dataframes = {}
for key, file_path in metadata_files.items():
    try:
        dataframes[key] = pd.read_csv(file_path)
        print(f"Loaded {key} successfully.")
    except Exception as e:
        print(f"Error loading {key}: {e}")

# Jinja2 Environment Setup
env = Environment(loader=FileSystemLoader('./templates'))

def generate_html(template_name, output_name, context):
    """ Generate an HTML page using a Jinja2 template. """
    template = env.get_template(template_name)
    rendered_html = template.render(context)
    with open(os.path.join(output_pages_dir, output_name), 'w', encoding='utf-8') as f:
        f.write(rendered_html)

# Example: Generating HTML Pages
# Generate Demographics Page
core_metrics_df = dataframes.get("core_metrics")
if core_metrics_df is not None:
    demographics_context = {
        "title": "Demographics Analysis",
        "college_distribution": core_metrics_df.to_dict(orient="records")
    }
    generate_html("demographics_template.html", "demographics.html", demographics_context)
    print("Demographics page generated.")

# Generate Evaluation Page
evaluation_df = dataframes.get("detailed_stats")
if evaluation_df is not None:
    evaluation_context = {
        "title": "Evaluation Analysis",
        "evaluation_data": evaluation_df.to_dict(orient="records")
    }
    generate_html("evaluation_template.html", "evaluation.html", evaluation_context)
    print("Evaluation page generated.")

# Add similar calls for other pages such as performance and findings.

print("HTML page generation completed.")
