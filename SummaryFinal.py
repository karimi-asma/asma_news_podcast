import json
from vertexai.preview.generative_models import GenerativeModel
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set environment variables
PROJECT_ID = os.getenv("GCP_PROJECT_ID")
REGION = os.getenv("GCP_REGION")

# Initialize Vertex AI
import vertexai
vertexai.init(project=PROJECT_ID, location=REGION)

def summarize_text_with_gemini(input_text):
    """
    Summarize text using Google's Gemini model via Vertex AI.

    Args:
        input_text (str): The input text to summarize.

    Returns:
        str: The summarized text.
    """
    # Initialize the Gemini model
    model = GenerativeModel("gemini-1.0-pro")

    # Use the model to generate a summary
    prompt = f"Summarize the following text in under 300 characters:\n\n{input_text}"
    response = model.generate_content(prompt)
    return response.text.strip()

def process_json_file(input_file, output_file):
    """
    Process a JSON file to summarize the 'content' field and add a 'summary' field.

    Args:
        input_file (str): Path to the input JSON file.
        output_file (str): Path to save the output JSON file with summaries.
    """
    with open(input_file, "r") as file:
        data = json.load(file)
    
    for entry in data:
        content = entry.get("content", "")
        print(f"Processing: {entry.get('title', 'No Title')}")
        
        # Check content length
        if len(content) < 200:
            print("Content length is less than 200 characters. Copying content to summary.")
            entry["summary"] = content
        else:
            try:
                print("Content length is sufficient. Generating summary...")
                summary = summarize_text_with_gemini(content)
                entry["summary"] = summary
            except Exception as e:
                print(f"Error summarizing '{entry.get('title', 'No Title')}': {e}")
                entry["summary"] = "Error generating summary."
    
    # Save the new JSON file with summaries
    with open(output_file, "w") as file:
        json.dump(data, file, indent=4)
    print(f"Summarized data saved to {output_file}")

# Example usage
if __name__ == "__main__":
    input_file = "news_articles.json"  # Replace with your input file path
    output_file = "output_data.json" # Replace with your desired output file path

    process_json_file(input_file, output_file)
