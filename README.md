# Asma News Podcast in Tech

A multi-agent AI project that automates the creation of tech-focused podcast episodes. This project leverages Agentic AI for content creation, including news scraping, summarization, script generation, and text-to-speech conversion.

## Features

- **News Scraping**: Fetches the latest tech news articles.
- **Summarization**: Condenses lengthy articles into concise summaries.
- **Script Generation**: Creates podcast-ready scripts.
- **Text-to-Speech**: Converts scripts into audio files.
- **Cloud Deployment**: Plans for deployment using AWS infrastructure.

## Requirements

- Python 3.8+
- Libraries: `requests`,`beautiful soup`, `transformers`, `torch`, `boto3`
- Hugging Face Transformers

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/asma-news-podcast-in-tech.git
   cd asma-news-podcast-in-tech
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run Agents Individually**:
   Execute each agent script to perform specific tasks like news scraping or summarization.
   ```bash
   python news_scraper.py
   python summarizer.py
   ```

2. **Integrate Agents**:
   Combine agents into a pipeline to automate the podcast creation workflow.

## Contribution

Feel free to fork the repository, create branches for new features, and submit pull requests.

## License


