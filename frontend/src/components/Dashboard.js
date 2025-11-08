import React, { useState, useEffect } from 'react';
import axios from 'axios';
import BiasChart from './BiasChart';
import ArticleList from './ArticleList';
import { Container, Row, Col, Button, Spinner, Alert } from 'react-bootstrap';

const BACKEND_URL = 'http://127.0.0.1:5000';

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [fetching, setFetching] = useState(false);

  useEffect(() => {
    fetchStats();
    fetchArticles();
  }, []);

  const fetchStats = async () => {
    try {
      setLoading(true);
      const res = await axios.get(`${BACKEND_URL}/api/stats`);
      if (res.data.success) {
        setStats(res.data.stats);
      } else {
        setError('Error fetching stats');
      }
    } catch (err) {
      setError('Backend not available or error fetching stats');
    }
    setLoading(false);
  };

  const fetchArticles = async () => {
    try {
      setLoading(true);
      const res = await axios.get(`${BACKEND_URL}/api/articles?limit=20`);
      if (res.data.success) {
        setArticles(res.data.articles || []);
      } else {
        setError('Error fetching articles');
      }
    } catch (err) {
      setError('Backend not available or error fetching articles');
    }
    setLoading(false);
  };

  const handleFetchNews = async () => {
    setFetching(true);
    setError('');
    try {
      await axios.post(`${BACKEND_URL}/api/fetch-news`, { limit: 2 });
      await fetchArticles();
      await fetchStats();
    } catch (err) {
      setError('Error triggering news fetch.');
    }
    setFetching(false);
  };

  return (
    <Container className="mt-4">
      <Row>
        <Col>
          <h2>News Bias Detector Dashboard</h2>
          <Button variant="primary" onClick={handleFetchNews} disabled={fetching || loading}>
            {fetching ? <Spinner size="sm" animation="border" /> : 'Fetch Latest News'}
          </Button>
        </Col>
      </Row>

      <Row>
        <Col>
          {error && <Alert variant="danger" className="mt-3">{error}</Alert>}
        </Col>
      </Row>

      <Row className="mt-4">
        <Col md={6}>
          {stats && <BiasChart stats={stats} />}
        </Col>
        <Col md={6}>
          <h5>Summary Stats</h5>
          {stats ? (
            <ul>
              <li><b>Total Articles:</b> {stats.total_articles}</li>
              <li><b>Avg Sentiment (Positive):</b> {stats.avg_sentiment.positive}</li>
              <li><b>Avg Sentiment (Negative):</b> {stats.avg_sentiment.negative}</li>
            </ul>
          ) : (
            <Spinner animation="border" />
          )}
        </Col>
      </Row>

      <Row className="mt-4">
        <Col>
          <ArticleList articles={articles} />
        </Col>
      </Row>
    </Container>
  );
}

export default Dashboard;
