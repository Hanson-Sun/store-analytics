import React from "react";
import { Button, Typography, Layout, Flex } from "antd";
import "./LandingPage.css";

const { Title } = Typography;
const { Content } = Layout;

function LandingPage() {
  return (
    <Layout className="landingpage">
      <Content>
        <div className="content-wrapper">
          <Flex vertical gap = "middle" direction="column" justify="center" align="center">
          <Title level={1} className="title" style={{ color: "white", padding: "10vh"}}>
            STORE ANALYTICS
          </Title>
          <Button size="large" type="primary" href="/homepage" className="get-started-button">
            Get Started
          </Button>
          </Flex>
        </div>
      </Content>
    </Layout>
  );
}

export default LandingPage;