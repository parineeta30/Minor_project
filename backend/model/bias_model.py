import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BiasDetector:
    def __init__(self):
        # Using pre-trained DistilBERT for sentiment analysis
        self.model_name = "distilbert-base-uncased-finetuned-sst-2-english"
        logger.info(f"Loading model: {self.model_name}")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            self.model.to(self.device)
            logger.info(f"Model loaded on device: {self.device}")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
        
        # Bias keywords for rule-based detection
        self.bias_keywords = {
            'left_leaning': [
                'progressive', 'liberal', 'inclusive', 'diversity', 
                'climate crisis', 'gun control', 'social justice',
                'activist', 'campaign', 'movement', 'fight for'
            ],
            'right_leaning': [
                'conservative', 'traditional values', 'law and order',
                'free market', 'border security', 'second amendment',
                'patriot', 'defense', 'America first', 'sovereignty'
            ],
            'propaganda': [
                'always', 'never', 'everyone knows', 'obviously',
                'clearly', 'undoubtedly', 'everyone agrees', 'everyone except',
                'shocking truth', 'they don\'t want you to know'
            ]
        }
    
    def analyze_sentiment(self, text):
        """Analyze sentiment using DistilBERT"""
        try:
            # Truncate text if too long
            if len(text) > 512:
                text = text[:512]
            
            inputs = self.tokenizer(
                text, 
                return_tensors="pt", 
                truncation=True, 
                max_length=512, 
                padding=True
            )
            
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            
            sentiment_scores = predictions[0].cpu().tolist()
            
            return {
                'negative': round(sentiment_scores[0], 4),
                'positive': round(sentiment_scores[1], 4),
                'overall': 'positive' if sentiment_scores[1] > sentiment_scores[0] else 'negative'
            }
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {e}")
            return {'negative': 0.5, 'positive': 0.5, 'overall': 'neutral'}
    
    def detect_bias(self, text):
        """Detect political bias using keyword analysis"""
        try:
            text_lower = text.lower()
            
            left_count = sum(1 for word in self.bias_keywords['left_leaning'] 
                            if word in text_lower)
            right_count = sum(1 for word in self.bias_keywords['right_leaning'] 
                             if word in text_lower)
            propaganda_count = sum(1 for word in self.bias_keywords['propaganda'] 
                                  if word in text_lower)
            
            total_bias_words = left_count + right_count
            
            if total_bias_words == 0:
                bias_type = 'neutral'
                bias_score = 0.0
            elif left_count > right_count:
                bias_type = 'left_leaning'
                bias_score = round(left_count / (left_count + right_count), 2)
            else:
                bias_type = 'right_leaning'
                bias_score = round(right_count / (left_count + right_count), 2)
            
            propaganda_score = round(propaganda_count / max(len(text.split()), 1), 4)
            
            return {
                'bias_type': bias_type,
                'bias_score': bias_score,
                'propaganda_score': propaganda_score,
                'left_keywords': left_count,
                'right_keywords': right_count,
                'propaganda_keywords': propaganda_count
            }
        except Exception as e:
            logger.error(f"Error in bias detection: {e}")
            return {
                'bias_type': 'unknown',
                'bias_score': 0.0,
                'propaganda_score': 0.0,
                'left_keywords': 0,
                'right_keywords': 0,
                'propaganda_keywords': 0
            }
    
    def analyze_article(self, article_text, title):
        """Complete analysis of an article"""
        try:
            # Combine title and text for better context
            full_text = f"{title}. {article_text}"
            
            # Limit to first 512 tokens for BERT
            if len(full_text.split()) > 512:
                full_text = ' '.join(full_text.split()[:512])
            
            sentiment = self.analyze_sentiment(full_text)
            bias = self.detect_bias(full_text)
            
            return {
                'sentiment': sentiment,
                'bias': bias,
                'analyzed_at': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error analyzing article: {e}")
            return {
                'sentiment': {'negative': 0.5, 'positive': 0.5, 'overall': 'neutral'},
                'bias': {
                    'bias_type': 'unknown',
                    'bias_score': 0.0,
                    'propaganda_score': 0.0,
                    'left_keywords': 0,
                    'right_keywords': 0,
                    'propaganda_keywords': 0
                },
                'analyzed_at': datetime.now().isoformat()
            }
