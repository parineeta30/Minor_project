import feedparser
import newspaper
from newspaper import Article
from datetime import datetime
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsScraper:
    def __init__(self):
        # RSS feeds from multiple news outlets
        self.feeds = {
            'cnn': 'http://rss.cnn.com/rss/cnn_topstories.rss',
            'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
            'fox': 'http://feeds.foxnews.com/foxnews/latest',
            'aljazeera': 'https://www.aljazeera.com/xml/rss/all.xml',
            'reuters': 'https://feeds.reuters.com/reuters/topNews',
        }
    
    def fetch_articles(self, source_name, limit=10):
        """Fetch articles from a specific RSS feed"""
        articles = []
        
        if source_name not in self.feeds:
            logger.error(f"Source {source_name} not found")
            return articles
        
        try:
            feed = feedparser.parse(self.feeds[source_name])
            logger.info(f"Fetching {limit} articles from {source_name}")
            
            for entry in feed.entries[:limit]:
                try:
                    # Extract basic info from RSS entry
                    article_data = {
                        'source': source_name,
                        'title': entry.get('title', 'No title'),
                        'url': entry.get('link', ''),
                        'published': entry.get('published', datetime.now().isoformat()),
                        'summary': entry.get('summary', ''),
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    # Try to download full article text
                    try:
                        article = Article(entry.link)
                        article.download()
                        article.parse()
                        article_data['text'] = article.text
                        article_data['authors'] = article.authors
                    except Exception as e:
                        logger.warning(f"Could not parse article {entry.link}: {e}")
                        article_data['text'] = entry.get('summary', '')
                        article_data['authors'] = []
                    
                    articles.append(article_data)
                    time.sleep(1)  # Rate limiting
                    
                except Exception as e:
                    logger.warning(f"Error processing entry: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Error fetching from {source_name}: {e}")
        
        return articles
    
    def fetch_all_sources(self, limit_per_source=5):
        """Fetch articles from all sources"""
        all_articles = []
        
        for source in self.feeds.keys():
            logger.info(f"Fetching from {source}...")
            articles = self.fetch_articles(source, limit=limit_per_source)
            all_articles.extend(articles)
            logger.info(f"Fetched {len(articles)} articles from {source}")
        
        logger.info(f"Total articles fetched: {len(all_articles)}")
        return all_articles
