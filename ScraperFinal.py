import requests
from bs4 import BeautifulSoup
import json
import time

class NewsScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "AsmaNewsScraper/1.0 (+mailto:asma@example.com)"
        }

    def fetch_articles(self, url, title_selector, content_selector=None, max_articles=5):
        """
        Fetches articles from the specified website.

        Args:
            url (str): The URL to scrape.
            title_selector (dict): CSS selector for article titles and links.
            content_selector (dict): CSS selector for article content.
            max_articles (int): Maximum number of articles to fetch.

        Returns:
            list: A list of articles with title, link, and content.
        """
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract titles and links
            articles = soup.find_all(**title_selector)[:max_articles]
            article_list = []

            for article in articles:
                title = article.get_text(strip=True)
                link = article['href']
                if not link.startswith('http'):  # Handle relative URLs
                    link = 'https://www.techcrunch.com' + link
                content = self.fetch_article_content(link, content_selector)
                article_list.append({'title': title, 'link': link, 'content': content})
                time.sleep(2)  # Rate-limiting to avoid overwhelming the server

            return article_list

        except requests.exceptions.RequestException as e:
            print(f"Error fetching articles from {url}: {e}")
            return []

    def fetch_article_content(self, url, content_selector):
        """
        Fetches the content of an article.

        Args:
            url (str): The article URL.
            content_selector (dict): CSS selector for article content.

        Returns:
            str: The full article content or an error message.
        """
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            if content_selector:
                # Find the parent container holding the article content
                content_container = soup.find(**content_selector)
                if content_container:
                    # Extract all <p> tags within the container
                    paragraphs = content_container.find_all('p')
                    if paragraphs:
                        # Concatenate the text from all paragraphs
                        full_content = ' '.join(p.get_text(strip=True) for p in paragraphs)
                        return full_content
            return "Content not found or format not supported."

        except requests.exceptions.RequestException as e:
            print(f"Error fetching content from {url}: {e}")
            return "Error fetching content."

    def save_to_json(self, articles, filename):
        """
        Saves articles to a JSON file.

        Args:
            articles (list): List of articles to save.
            filename (str): Name of the JSON file.
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=4)
        print(f"Articles saved to {filename}")

# Example Usage
if __name__ == "__main__":
    scraper = NewsScraper()

    # TechCrunch
    techcrunch_articles = scraper.fetch_articles(
        url="https://techcrunch.com/",
        title_selector={"name": "a", "class_": "loop-card__title-link"},
        content_selector={"name": "div", "class_": "entry-content"}
    )

    # Save to JSON
    scraper.save_to_json(techcrunch_articles, "news_articles.json")
