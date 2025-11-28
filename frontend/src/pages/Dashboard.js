import React, { useState, useEffect } from 'react';
import ResumeUpload from '../components/ResumeUpload';
import CandidateTable from '../components/CandidateTable';
import { candidateService } from '../services/api';
import './Dashboard.css';

const Dashboard = () => {
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchCandidates = async () => {
    try {
      setLoading(true);
      const data = await candidateService.getCandidates();
      setCandidates(data.candidates);
      setError(null);
    } catch (err) {
      setError('Failed to load candidates');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCandidates();
  }, []);

  const handleUploadSuccess = (newCandidate) => {
    setCandidates([newCandidate, ...candidates]);
  };

  return (
    <div className="dashboard">
      <div className="dashboard-content">
        <section className="upload-section">
          <h2>Upload Resume</h2>
          <ResumeUpload onUploadSuccess={handleUploadSuccess} />
        </section>

        <section className="candidates-section">
          <div className="section-header">
            <h2>Candidates</h2>
            <span className="candidate-count">{candidates.length} Total</span>
          </div>
          {loading ? (
            <div className="loading">Loading candidates...</div>
          ) : error ? (
            <div className="error">{error}</div>
          ) : (
            <CandidateTable candidates={candidates} />
          )}
        </section>
      </div>
    </div>
  );
};

export default Dashboard;
