"""
title: News Summarizer
author: Pat Dalberg
author_url: https://website.com
git_url: https://github.com/username/news-summarizer.git
description: This Open WebUI tool fetches and summarizes the latest 5 articles from news.ycombinator.com
required_open_webui_version: 0.1.0
requirements: Open WebUI
version: 0.1.0
licence: MIT
"""

from pydantic import BaseModel, Field
import requests
from transformers import pipeline

class Tools:
    def __init__(self):
        """Initialize the Tool."""
        self.valves = self.Valves()
    
    class Valves(BaseModel):
        api_key: str = Field("", description="Your API key here")
    
    def get_news(self) -> list:
        """
        Fetches the 5 latest articles from news.ycombinator.com.
        """
        url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
        response = requests.get(url)
        story_ids = response.json()[:5]

        news_items = []
        for story_id in story_ids:
            story_url = f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json'
            story_response = requests.get(story_url)
            story_data = story_response.json()

            if 'url' in story_data and 'title' in story_data:
                full_article = requests.get(story_data['url']).text
                news_items.append({
                    'id': story_id,
                    'title': story_data['title'],
                    'url': story_data['url'],
                    'content': full_article
                })

        return news_items
    
    def summarize_news(self, articles: list) -> list:
        """
        Summarizes the fetched articles using a pre-trained summarization model.
        """
        summarizer = pipeline("summarization")
        
        summarized_articles = []
        for article in articles:
            summary = summarizer(article['content'], max_length=150, min_length=30, do_sample=False)[0]['summary_text']
            summarized_articles.append({
                'id': article['id'],
                'title': article['title'],
                'url': article['url'],
                'summary': summary
            })

        return summarized_articles
    
    def main(self):
        """
        Main method to fetch and summarize the news.
        """
        articles = self.get_news()
        summarized_articles = self.summarize_news(articles)
        
        return summarized_articles
