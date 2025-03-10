import React from "react";
import "./Researchhomepage.css";
import { useNavigate } from "react-router-dom";
export function Researchhomepage() {
  const navigate = useNavigate();
  return (
    <div className="research-homepage-container">
      {/* Header Section */}
      <header className="research-homepage-header">
        <h1 className="research-homepage-title">Research Pulse</h1>
        <p className="research-homepage-subtitle">
          Your institution's one-stop solution for research insights, with more institutions coming soon.
        </p>
      </header>

      {/* Buttons Section */}
      <div className="research-homepage-buttons-container">
        <div className="research-homepage-button-card">
          <button className="research-homepage-btn"  onClick={() => navigate("/research-chatbot-student")}>For Students</button>
          <p>
            Access exclusive research insights for your institution, track departmental collaborations, and explore how different faculties work together to drive innovation.
          </p>
        </div>

        <div className="research-homepage-button-card">
        <button 
      className="research-homepage-btn" 
      onClick={() => navigate("/research-chatbot-professor")}
    >For professors</button>
          <p>
            Gain in-depth research analytics specific to your institution, oversee academic publications, and identify key interdisciplinary collaborations within your university.
          </p>
        </div>

        <div className="research-homepage-button-card">
          <button className="research-homepage-btn" onClick={() => navigate("/research-chatbot-benefactor")}>For Benefactors</button>
          <p>
            Support groundbreaking research projects at your institution and soon across multiple universities, fostering innovation and academic excellence.
          </p>
        </div>
      </div>
    </div>
  );
}
