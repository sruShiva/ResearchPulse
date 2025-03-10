import logo from './logo.svg';
import './App.css';
import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import {Researchhomepage} from './Researchhompage'
import { ResearchChatbot } from './Researchchatbot';

export function App() {
  return (
    <Router>

      <Routes>
        <Route path="/" element={<Researchhomepage />} />
        </Routes>

        <Routes>
        <Route path="/research-chatbot-student" element={<ResearchChatbot persona="student" />} />
      </Routes>

      <Routes>
        <Route path="/research-chatbot-professor" element={<ResearchChatbot persona="professor" />} />
      </Routes>
      
      <Routes>
        <Route path="/research-chatbot-benefactor" element={<ResearchChatbot persona="benefactor" />} />
      </Routes>
     
    </Router>
  );
}

export default App;
