import React, { useEffect, useState } from 'react';
import { Card, Col, Row } from 'antd';


const BarChartCustomers = () => {

  const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
  
    useEffect(() => {
      const fetchData = async () => {
        try {
          const response = await fetch('http://localhost:8000/api/unique_objects_per_hour');
          if (response.ok) {
            const result = await response.json();
            setData(result);
          } else {
            console.error('Error fetching data:', response.statusText);
          }
          setLoading(false);
        } catch (error) {
          console.error('Error fetching data:', error);
          setLoading(false);
        }
      };
  
      fetchData();
    }, []);

  return (
    <Row>
      <Col span={24}>
        <Card title="Unique Objects Per Hour" bordered={false} loading={loading}>
          {Object.keys(data).length > 0 ? (
            <ul>
              {Object.entries(data).map(([hour, count]) => (
                <li key={hour}>
                  Hour {hour}: {count} unique objects
                </li>
              ))}
            </ul>
          ) : (
            <p>No data available</p>
          )}
        </Card>
      </Col>
    </Row>
  );
};

export default BarChartCustomers;