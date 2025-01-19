import "./HomePage.css"
import { Button, Flex } from 'antd';
import React, { useState } from 'react';
import { Layout, Typography, Card, Progress, Row, Col, Statistic, Input } from 'antd';
import VideoFeed from "../component/VideoFeed"
import BarChartCustomers from '../component/BarChartCustomers';
import HeatmapExample from '../component/HeatMapG';

const { Header, Content } = Layout;
const { Title, Text } = Typography;

const xLabels = new Array(24).fill(0).map((_, i) => `${i}`)
const yLabels = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri']
const data = new Array(yLabels.length)
    .fill(0)
    .map(() =>
        new Array(xLabels.length).fill(0).map(() => Math.floor(Math.random() * 50 + 50))
    )

function HomePage() {

    const currentPeopleCount = 50;
    let time = new Date().toLocaleTimeString()

    const [ctime, setTime] = useState(time)
    const UpdateTime = () => {
        time = new Date().toLocaleTimeString()
        setTime(time)
    }
    setInterval(UpdateTime)

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
                            <VideoFeed />
                        </Card>
                    </Col>

                    <Col span={8}>
                        <Card title="Mean Heatmap" bordered={false}>
                            <HeatmapExample />
                        </Card>
                    </Col>

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
