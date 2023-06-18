import React from 'react';
import './Landing.css'; // Import the CSS file for component-specific styles

function Landing() {
  const handleButton = ()=>{
    window.location.href = "http://localhost:3000/learn"
  }
  return (
    <div className="landing-container">
      <h1 className="logo-text">Learn English with AI</h1>
      <button className="get-started-button" onClick={handleButton}>Get Started</button>
    </div>
  );
}

export default Landing;
