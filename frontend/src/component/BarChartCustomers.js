import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

// Example data with time (you can use actual time data or timestamps)
const data = [
  { time: '10:00 AM', customers: 50 },
  { time: '11:00 AM', customers: 65 },
  { time: '12:00 PM', customers: 80 },
  { time: '01:00 PM', customers: 120 },
  { time: '02:00 PM', customers: 140 },
  { time: '03:00 PM', customers: 100 },
  { time: '04:00 PM', customers: 90 },
];

const BarChartCustomers = () => {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="time" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="customers" fill="#8884d8" />
      </BarChart>
    </ResponsiveContainer>
  );
};

export default BarChartCustomers;