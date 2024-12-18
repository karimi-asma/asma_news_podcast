Asma News Podcast in Tech
A multi-agent AI project that automates the creation of tech-focused podcast episodes. This project leverages Agentic AI to streamline the end-to-end workflow, including news scraping, summarization, script generation, and text-to-speech conversion.

Features
News Scraping: Automatically fetches the latest tech news articles from specified websites.
Summarization: Condenses lengthy articles into concise and informative summaries.
Script Generation: Creates podcast-ready scripts with engaging content, incorporating technical details and a natural flow.
Text-to-Speech Conversion: Converts podcast scripts into high-quality audio files using Google Cloud Text-to-Speech.
Cloud Deployment: Supports deployment on Google Cloud Platform (GCP) and AWS, including integration with Vertex AI for script generation.
Requirements
Python: Version 3.8 or higher.
Libraries:
requests
beautifulsoup4
transformers
torch
google-cloud-texttospeech
gtts
dotenv
vertexai
Cloud Requirements:
Google Cloud Text-to-Speech API enabled.
Google Vertex AI enabled for script generation.
Installation
1. Clone the Repository:

git clone https://github.com/karimi-asma/asma_news_podcast.git
cd asma-news-podcast
2. Install Dependencies:
Install the required Python libraries:

pip install -r requirements.txt

Usage
1. Run Agents Individually:
Execute each agent to perform specific tasks:

News Scraping:
python src/ScraperFinal.py
Script Generation and Text-to-Speech:

python src/ScriptAudio.py
2. Pipeline Integration:
Combine all agents into a cohesive pipeline to automate the entire podcast creation workflow:


python pipeline/main_pipeline.py
Cloud Deployment
Google Cloud Platform (GCP):
Use Vertex AI for script generation.
Use Google Cloud Text-to-Speech for high-quality audio conversion.
Future Plans for AWS:
Automate the pipeline using AWS Lambda, S3, and Step Functions.
Incorporate cost-effective deployment options using Bedrock.

Contribution
We welcome contributions! Feel free to fork the repository, create feature branches, and submit pull requests.

License
This project is licensed under the MIT License
