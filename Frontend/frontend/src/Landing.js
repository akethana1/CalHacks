import React from 'react';
import './Landing.css';
import Navbar from './nav_bar'; // Import the CSS file for component-specific styles

function Landing() {
  const handleButton = ()=>{
    window.location.href = "http://localhost:3001/learn"
  }
  return (
    <div className="landing-container">
      <Navbar />
      <h1 className="starting-text">Real-time Feedback on English Speaking</h1>
      <h2 className="mission-text">
        An issue exists with non-native English speakers: how to properly respond in 
        real-world conversations. With AI, we simulate an environment for users to practice their English
        and receive real-time feedback.
      </h2>
      <button className="get-started-button" onClick={handleButton}>Get Started</button>
    </div>
  );
}

export default Landing;
