import os
import json
import re
from dotenv import load_dotenv
from vertexai.generative_models import GenerativeModel
from gtts import gTTS
import vertexai
from google.cloud import texttospeech

# Load environment variables
load_dotenv()
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
PROJECT_ID = os.getenv("GCP_PROJECT_ID")
LOCATION = os.getenv("GCP_REGION")

# Initialize Vertex AI
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Load JSON file
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Clean Podcast Script
def clean_text(text):
    """
    Cleans the podcast script to make it suitable for text-to-speech.
    Removes markdown symbols, labels, and special cues.
    """
    # Step 1: Remove Markdown headers (##, **, etc.)
    text = re.sub(r'[#*]+', '', text)  # Remove # and * symbols
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Remove ** around words
    
    # Step 2: Remove section labels like "Host:"
    text = re.sub(r'\b(H|h)ost:\s*', '', text)
    
    # Step 3: Remove content in parentheses (e.g., "(Upbeat music fades in)")
    text = re.sub(r'\(.*?\)', '', text)
    
    # Step 4: Remove extra spaces and blank lines
    text = re.sub(r'\n+', '\n', text)  # Remove extra newlines
    text = re.sub(r'\s{2,}', ' ', text)  # Replace multiple spaces with a single space

    # Step 5: Remove music-related parts (e.g., Intro Music, Outro Music Fades)
    text = re.sub(r'(?i)\b(Intro Music|Outro Music|Outro Music Fades)\b', '', text)

    # Step 6: Trim whitespace
    text = text.strip()
    
    return text

# Generate cohesive Podcast Script using Gemini
def generate_combined_script(summaries):
    # Combine summaries into a single input for Gemini
    combined_input = "\n\n".join([f"Article {i+1}: {summary}" for i, summary in enumerate(summaries)])

    # Prompt for Gemini
    prompt = f"""
    You're a podcast script writer tasked with creating a technical, yet amusing and catchy podcast episode.
    Use the following summaries of articles to write a single cohesive podcast script. Make it engaging, informative, 
    and flow naturally like a story while retaining the technical details:
    
    {combined_input}

    Start with a hook, include fun facts or light humor where appropriate, and conclude with a strong ending.
    """
    # Generate content using Gemini
    model = GenerativeModel("gemini-1.0-pro")  # Use the latest Gemini model
    response = model.generate_content(prompt)
    return response.text if response else "Failed to generate script."

# Convert Script to Speech
# def text_to_speech(script, output_file):
#     tts = gTTS(script, lang="en")
#     tts.save(output_file)
#     print(f"Audio saved as: {output_file}")


def text_to_speech(script, output_file):
    """
    Converts text to high-quality speech using Google Cloud Text-to-Speech.
    """
    # Initialize the TTS client
    client = texttospeech.TextToSpeechClient()

    # Prepare the input text
    synthesis_input = texttospeech.SynthesisInput(text=script)

    # Configure the voice
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",  # Language
        name="en-US-Wavenet-F",  # Wavenet voice for natural sound
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    # Configure audio settings
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.0,  # Adjust the speed if necessary
        pitch=0.0  # Adjust the pitch for better tone
    )

    # Generate speech
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Save the audio to an output file
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print(f"Audio content written to file: {output_file}")


# Main Function
if __name__ == "__main__":
    # Load JSON file
    json_file_path = "output_data.json"  # Replace with your file path
    data = load_json(json_file_path)

    # Extract summaries from JSON
    summaries = []
    for article in data:
        summary = article.get("summary")
        if summary:
            summaries.append(summary)
    
    # Generate podcast script
    print("Generating cohesive podcast script...")
    podcast_script = generate_combined_script(summaries)
    print("Original Script:\n", podcast_script)
    
    # Clean the script
    print("\nCleaning the podcast script...")
    cleaned_script = clean_text(podcast_script)
    print("Cleaned Script:\n", cleaned_script)
    
    # Convert the cleaned script to audio
    print("\nConverting script to audio...")
    output_audio = "podcast_output.mp3"
    text_to_speech(cleaned_script, output_audio)
    print("Process completed successfully!")
