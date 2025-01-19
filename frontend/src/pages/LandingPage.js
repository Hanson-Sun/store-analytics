import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, Typography, Layout, Space, Input, Flex } from "antd";
import "./LandingPage.css";

const { Title } = Typography;
const { Content } = Layout;

function LandingPage() {

  const [cameraUrl, setCameraUrl] = useState("");
  const navigate = useNavigate();

  const handleGetStarted = async () => {
    try {
      const response = await fetch('http://localhost:5000/set_camera_url', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: cameraUrl }),
      });

      const result = await response.json();
      if (result.status === "success") {
        navigate("/homepage");
      } else {
        alert(result.result);
      }
    } catch (error) {
      console.error("Error setting camera URL:", error);
    }
  };
  
  return (
    <Layout className="landingpage">
      <Content>
          <Space direction="vertical" size="middle" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
          <Flex vertical gap = "middle" direction="column" justify="center" align="center">
          <Title level={1} className="title" style={{ color: "white", padding: "10vh"}}>
            STORE ANALYTICS
          </Title>
          <Input 
              placeholder="Enter Camera IP" 
              value={cameraUrl} 
              onChange={(e) => setCameraUrl(e.target.value)} 
            />
          <Button size="large" type="primary"onClick={handleGetStarted} className="get-started-button">
            Get Started
          </Button>
          </Flex>
        </Space>
      </Content>
    </Layout>
  );
}

export default LandingPage;