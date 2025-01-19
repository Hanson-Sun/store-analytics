import "./HomePage.css"
import { Button, Flex } from 'antd';
import React from 'react';
import { Layout, Typography, Card, Progress, Row, Col, Statistic } from 'antd';
import { LineChartOutlined, HeatMapOutlined } from '@ant-design/icons';

import BarChartCustomers from '../component/BarChartCustomers';
import VideoFeed from '../component/VideoFeed';

const { Header, Content } = Layout;
const { Title, Text } = Typography;

function HomePage() {

    const currentPeopleCount = 50;

    return (
        <Layout style={{ minHeight: '100vh' }}>
            <Header style={{ background: '#001529', padding: 0, margins: 10}}>
                <div style={{ color: 'white', textAlign: 'center', fontSize: '40px', padding: '10px' }}>
                    STORE ANALYTICS
                </div>
            </Header>

            <Content style={{ padding: '20px' }}>
                <Title level={2}>Store Analytics Dashboard</Title>

                <Row gutter={16}>
                    <Col span={8}>
                        <Card title="Live Feed" bordered={false}>
                            <VideoFeed />
                        </Card>
                    </Col>

                    <Col span={8}>
                        <Card title="Mean Heatmap" bordered={false}>
                            <HeatMapOutlined style={{ fontSize: '40px', color: '#52c41a' }} />
                            <Text>Heatmap of store activity will be displayed here.</Text>
                        </Card>
                    </Col>

                    <Col span={8}>
                        <Card title="Number of People in Store" bordered={false}>
                            <Row gutter={16}>
                                <Col span={12}>
                                    <Statistic title="People Count" value={currentPeopleCount} />
                                </Col>
                            </Row>
                        </Card>
                    </Col>
                </Row>

                <Row style={{ marginTop: '20px' }} gutter={16}>
                    <Col span={24}>
                        <Card title="Average Store Traffic Over Time" bordered={false}>
                            <LineChartOutlined style={{ fontSize: '40px', color: '#1890ff' }} />
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
