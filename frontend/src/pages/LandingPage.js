import "./LandingPage.css";
import { Button, Flex } from 'antd';

function LandingPage() {
  return (
   <Flex vertical gap="middle" justify="center" align="center" classname = "landingpage">
        <div classname = "Title">
            STORE ANALYTICS 
        </div>
        <Button size = "large" type="primary" href="/homepage">Get Started</Button>    
   </Flex>
  );
}

export default LandingPage;