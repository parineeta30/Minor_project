import React from 'react';
import { PieChart, Pie, Cell, Legend, Tooltip, ResponsiveContainer } from 'recharts';

const COLORS = {
  left_leaning: '#0088FE',
  right_leaning: '#FF8042',
  neutral: '#00C49F'
};

function BiasChart({ stats }) {
  const data = [
    { name: 'Left Leaning', value: stats.bias_distribution.left_leaning },
    { name: 'Right Leaning', value: stats.bias_distribution.right_leaning },
    { name: 'Neutral', value: stats.bias_distribution.neutral }
  ];

  return (
    <div>
      <h5>Bias Distribution</h5>
      <ResponsiveContainer width="100%" height={250}>
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={80}
            label
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[entry.name.toLowerCase().replace(' ', '_')] || '#888'} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

export default BiasChart;
