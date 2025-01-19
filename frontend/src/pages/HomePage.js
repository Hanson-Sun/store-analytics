import "./HomePage.css"
import { Button, Flex } from 'antd';
import React, { useState, useEffect} from 'react';
import { Layout, Typography, Card, Progress, Row, Col, Statistic, Input } from 'antd';
import VideoFeed from "../component/VideoFeed"
import BarChartCustomers from '../component/BarChartCustomers';
import HeatmapExample from '../component/HeatMapG';
import { Heatmap } from "heatmap.js";

const { Header, Content } = Layout;
const { Title, Text } = Typography;

function HomePage() {
    const [currentPeopleCount, setCurrentPeopleCount] = useState(0);
    let time = new Date().toLocaleTimeString()

    const [ctime, setTime] = useState(time)
    const UpdateTime = () => {
        time = new Date().toLocaleTimeString()
        setTime(time)
    }
    setInterval(UpdateTime)

    useEffect(() => {
        const fetchPeopleCount = async () => {
          try {
            const endTime = new Date().toISOString(); // Current time in ISO format
            const startTime = new Date(Date.now() - 2000).toISOString(); // 2 seconds ago
    
            const response = await fetch(
              `http://localhost:8000/api/count_unique_objects?start_time=${startTime}&end_time=${endTime}`
            );
            if (!response.ok) {
              throw new Error(`API error: ${response.status}`);
            }
            const data = await response.json();
            setCurrentPeopleCount(data.result || 0); // Update the people count
          } catch (error) {
            console.error('Error fetching people count:', error);
          }
        };
    
        const interval = setInterval(fetchPeopleCount, 2000); // Fetch every 2 seconds
    
        return () => clearInterval(interval); // Cleanup on component unmount
      }, []);
    

    return (
        <Layout style={{ minHeight: '100vh', maxHeight: "100vh" }}>
            <Header style={{ background: '#001529', padding: 0, margins: 10 }}>
                <div style={{ color: 'white', textAlign: 'center', fontSize: '40px', padding: '10px' }}>
                    STORE ANALYTICS
                </div>
            </Header>

            <Content style={{ padding: '20px' }}>
                <Title level={2}>Store Analytics Dashboard</Title>

                <Row gutter={16}>
                    <Col span={8}>
                        <Card title="Live Feed" bordered={false}>
                            <div>
                            <VideoFeed />
                            </div>
                        </Card>
                    </Col>

                    {/* <Col span={8}>
                        <Card title="Mean Heatmap" bordered={false}>
                            <HeatmapExample />
                        </Card>
                    </Col> */}

                    <Col span={8}>
                        <Card title="Number of People in Store" bordered={false}>
                            <Row gutter={16}>
                                <Col span={12}>
                                    <Statistic title="People Count" value={currentPeopleCount} />
                                    <Statistic title="Time" value={ctime} />
                                </Col>
                            </Row>
                        </Card>
                    </Col>
                </Row>

                <Row style={{ marginTop: '20px' }} gutter={16}>
                    <Col span={24}>
                        <Card title="Average Store Traffic Over Time" bordered={false}>
                            <div>
                                <BarChartCustomers />
                            </div>
                        </Card>
                    </Col>
                </Row>
            </Content>
        </Layout>
    );
}

export default HomePage;
