from flask import Flask, jsonify, request
from flask_cors import CORS
from scrapers.news_scraper import NewsScraper
from model.bias_model import BiasDetector
from datetime import datetime
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize components
try:
    scraper = NewsScraper()
    detector = BiasDetector()
    logger.info("Components initialized successfully")
except Exception as e:
    logger.error(f"Error initializing components: {e}")
    scraper = None
    detector = None

# In-memory storage (for testing without Firebase)
articles_db = []

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'components': {
            'scraper': 'initialized' if scraper else 'failed',
            'detector': 'initialized' if detector else 'failed'
        }
    })

@app.route('/api/fetch-news', methods=['POST'])
def fetch_news():
    """Fetch and analyze news from all sources"""
    try:
        if not scraper or not detector:
            return jsonify({'success': False, 'error': 'Components not initialized'}), 500
        
        data = request.json or {}
        limit = data.get('limit', 5)
        
        logger.info(f"Fetching news with limit {limit} per source")
        
        # Fetch articles
        articles = scraper.fetch_all_sources(limit_per_source=limit)
        
        if not articles:
            return jsonify({'success': False, 'error': 'No articles fetched'}), 400
        
        # Analyze each article
        analyzed_articles = []
        for article in articles:
            try:
                # Skip articles without text
                if not article.get('text') and not article.get('summary'):
                    logger.warning(f"Skipping article without content: {article.get('title')}")
                    continue
                
                text = article.get('text') or article.get('summary', '')
                title = article.get('title', '')
                
                analysis = detector.analyze_article(text, title)
                
                article_with_analysis = {
                    **article,
                    **analysis
                }
                
                analyzed_articles.append(article_with_analysis)
                articles_db.append(article_with_analysis)
                
                logger.info(f"Analyzed: {article.get('source')} - {title[:50]}")
                
            except Exception as e:
                logger.warning(f"Error analyzing article: {e}")
                continue
        
        return jsonify({
            'success': True,
            'count': len(analyzed_articles),
            'articles': analyzed_articles
        })
    
    except Exception as e:
        logger.error(f"Error in fetch_news: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/articles', methods=['GET'])
def get_articles():
    """Get stored articles"""
    try:
        source = request.args.get('source')
        limit = int(request.args.get('limit', 50))
        
        # Filter articles
        filtered_articles = articles_db
        
        if source:
            filtered_articles = [a for a in filtered_articles if a.get('source') == source]
        
        # Return limited articles
        return jsonify({
            'success': True,
            'count': len(filtered_articles[:limit]),
            'articles': filtered_articles[:limit]
        })
    
    except Exception as e:
        logger.error(f"Error in get_articles: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/analyze-text', methods=['POST'])
def analyze_text():
    """Analyze custom text for bias"""
    try:
        if not detector:
            return jsonify({'success': False, 'error': 'Detector not initialized'}), 500
        
        data = request.json or {}
        text = data.get('text', '')
        title = data.get('title', 'Custom Text')
        
        if not text:
            return jsonify({'success': False, 'error': 'No text provided'}), 400
        
        analysis = detector.analyze_article(text, title)
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
    
    except Exception as e:
        logger.error(f"Error in analyze_text: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_statistics():
    """Get bias statistics across sources"""
    try:
        if not articles_db:
            return jsonify({
                'success': True,
                'stats': {
                    'total_articles': 0,
                    'by_source': {},
                    'bias_distribution': {'left_leaning': 0, 'right_leaning': 0, 'neutral': 0},
                    'avg_sentiment': {'positive': 0.0, 'negative': 0.0}
                }
            })
        
        stats = {
            'total_articles': len(articles_db),
            'by_source': {},
            'bias_distribution': {
                'left_leaning': 0,
                'right_leaning': 0,
                'neutral': 0
            },
            'avg_sentiment': {'positive': 0.0, 'negative': 0.0}
        }
        
        for article in articles_db:
            # Source stats
            source = article.get('source', 'unknown')
            if source not in stats['by_source']:
                stats['by_source'][source] = 0
            stats['by_source'][source] += 1
            
            # Bias distribution
            bias_type = article.get('bias', {}).get('bias_type', 'neutral')
            if bias_type in stats['bias_distribution']:
                stats['bias_distribution'][bias_type] += 1
            
            # Sentiment
            sentiment = article.get('sentiment', {})
            stats['avg_sentiment']['positive'] += sentiment.get('positive', 0.0)
            stats['avg_sentiment']['negative'] += sentiment.get('negative', 0.0)
        
        # Calculate averages
        if stats['total_articles'] > 0:
            stats['avg_sentiment']['positive'] = round(stats['avg_sentiment']['positive'] / stats['total_articles'], 4)
            stats['avg_sentiment']['negative'] = round(stats['avg_sentiment']['negative'] / stats['total_articles'], 4)
        
        return jsonify({
            'success': True,
            'stats': stats
        })
    
    except Exception as e:
        logger.error(f"Error in get_statistics: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/clear', methods=['POST'])
def clear_articles():
    """Clear all stored articles"""
    global articles_db
    articles_db = []
    return jsonify({'success': True, 'message': 'All articles cleared'})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'
    logger.info(f"Starting Flask app on port {port}")
    app.run(debug=debug, host='0.0.0.0', port=port)
