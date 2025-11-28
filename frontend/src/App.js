import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import CandidateProfile from './pages/CandidateProfile';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/candidate/:id" element={<CandidateProfile />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
