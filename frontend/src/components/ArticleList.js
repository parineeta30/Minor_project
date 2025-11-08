import React from 'react';
import { Table } from 'react-bootstrap';

function ArticleList({ articles }) {
  if (!articles.length) {
    return <div>No articles to display.</div>;
  }

  return (
    <div>
      <h5>Recent Articles</h5>
      <Table striped bordered hover responsive>
        <thead>
          <tr>
            <th>Source</th>
            <th>Title</th>
            <th>Bias</th>
            <th>Sentiment</th>
            <th>Link</th>
          </tr>
        </thead>
        <tbody>
          {articles.map((article, idx) => (
            <tr key={idx}>
              <td>{article.source}</td>
              <td>{article.title}</td>
              <td>
                {article.bias?.bias_type || "N/A"}
                {article.bias && article.bias.bias_score != null
                  ? ` (${Math.round(article.bias.bias_score * 100)}%)`
                  : ""}
              </td>
              <td>{article.sentiment?.overall || "N/A"}</td>
              <td>
                <a href={article.url} target="_blank" rel="noopener noreferrer">View</a>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
}

export default ArticleList;
