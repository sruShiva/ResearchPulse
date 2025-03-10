import React, { useState, useEffect } from "react";
import "./Researchchatbot.css";
import axios from "axios";


export function ResearchChatbot({ persona }) {
  
      
  const [chatMessages, setChatMessages] = useState([]);
  const [userInput, setUserInput] = useState("");

  const personas = {
    student: {
      title: "Student",
      subtext: "Explore research & career opportunities",
      tabs: {
        graph: "Understanding University departments and Research",
        general: "Job & Career Pathways",
      },
      questions: {
        graph: [
          "Which departments have the most communication?",
          "Which teams have the strongest communication links within the organization?",
        ],
        general: [
          "What are career paths are trending the industry now?",
          "What would be the most suitable field of research for me based on my interest in biology?",
        ],
      },
    },
    professor: {
      title: "Professor",
      subtext: "Discover research collaboration opportunities",
      tabs: {
        graph: "Identifying Potential Research Prospects in the institution",
        general: "Finding the Right Research Role and Collaborators",
      },
      questions: {
        graph: [
          "Which departments collaborate most frequently on research projects?",
          "How can I identify potential interdisciplinary research partners?",
        ],
        general: [
          "Which universities have research interests similar to mine which is in mathematics?",
         "Which department has the most students interested in collaborating on mathematics research?"
        ],
      },
    },
    benefactor: {
      title: "Benefactor",
      subtext: "Support and fund impactful research initiatives",
      tabs: {
       "graph": "Evaluating the Impact of Interdepartmental Research",
    "general": "Understanding Grant Distribution & Effective Allocation"
      },
      questions: {
        "graph": [
            "Which department has maxiumum collaborations?",
            "How does connections between departments affect my funding"
          ],
          "general": [
            "Which departments receive the most research funding, and how is it utilized?",
            "What are the key factors in ensuring effective grant allocation for maximum impact?"
          ]
      },
    },
  };
  const [activeTab, setActiveTab] = useState(
    Object.keys(personas[persona].tabs)[0] // Sets first tab dynamically
  );
 

  const handleSendMessage = async (tab, persona) => {
    if (userInput.trim() === "") return; // Prevent empty messages
  
    // Append user message to chat
    const updatedChat = [...chatMessages, { sender: "User", text: userInput }];
    setChatMessages(updatedChat);
    setUserInput(""); // Clear input field
  
    // Show loading message
    const loadingMessage = { sender: "Bot", text: "Our research assistant is thinking and curating the most suitable response for you..." };
    setChatMessages([...updatedChat, loadingMessage]);
  
    try {
      // Define API endpoints for each persona
      const apiUrls = {
        student: "http://localhost:8000/api/answer-student-queries",
        professor: "http://localhost:8000/api/answer-professor-queries",
        benefactor: "http://localhost:8000/api/answer-benefactor-queries"
      };
  
      // Select API based on persona
      const apiUrl = apiUrls[persona] || apiUrls["student"]; // Default to student
      console.log(apiUrl);
      console.log(persona, tab, userInput);
  
      // Send request to backend
      const response = await axios.get(apiUrl, {
        headers: {
          "Content-Type": "application/json",
        },
        params: {
          intention: tab,
          query: userInput,
        },
      });
  
      // Remove loading message and append bot response
      const botMessage = { sender: "Bot", text: response.data };
      setChatMessages([...updatedChat, botMessage]);
    } catch (error) {
      console.error("Error fetching bot response:", error);
  
      // Show error message instead of loading message
      setChatMessages([
        ...updatedChat,
        { sender: "Bot", text: "Error fetching response. Please try again!" },
      ]);
    }
  };
  
  
  

  const handleKeyDown = (e) => {
    if (e.key === "Enter") handleSendMessage();
  };

  return (
    <div className="research-chatbot-container">
      {/* Left Panel: Tabs & Suggested Questions */}
      <div className="research-chatbot-left">
        <h2>{personas[persona].title}</h2>
        <p className="research-chatbot-subtext">{personas[persona].subtext}</p>

        <div className="research-chatbot-tabs">
          {Object.keys(personas[persona].tabs).map((tabKey) => (
            <button
              key={tabKey}
              className={`research-chatbot-tab-btn ${activeTab === tabKey ? "active" : ""}`}
              onClick={() => setActiveTab(tabKey)}
            >
              {personas[persona].tabs[tabKey]}
            </button>
          ))}
        </div>

        <h3 className="research-chatbot-suggested-header">Suggested Questions</h3>
        <div className="research-chatbot-suggestions">
          {personas[persona].questions[activeTab].map((q, index) => (
            <div
              key={index}
              className="research-chatbot-suggestion"
              onClick={() => setUserInput(q)}
            >
              {q}
            </div>
          ))}
        </div>
      </div>

      {/* Right Panel: Chatbot */}
      <div className="research-chatbot-right">
        <div className="research-chatbot-messages">
          {chatMessages.map((msg, index) => (
            <div key={index} className={`research-chatbot-message ${msg.sender.toLowerCase()}`}>
              {msg.text}
            </div>
          ))}
        </div>
        <div className="research-chatbot-input-box">
          <input
            type="text"
            className="research-chatbot-input"
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            placeholder="Type a message..."
            onKeyDown={handleKeyDown}
          />
        <button 
        className="research-chatbot-send-btn" 
        onClick={() => handleSendMessage(activeTab, persona)}
        >
        ➤
        </button>
        </div>
      </div>
    </div>
  );
}
