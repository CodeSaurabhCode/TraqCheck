import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { candidateService } from '../services/api';
import './CandidateProfile.css';

const CandidateProfile = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [candidate, setCandidate] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [requesting, setRequesting] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [requestResult, setRequestResult] = useState(null);
  const [panFile, setPanFile] = useState(null);
  const [aadhaarFile, setAadhaarFile] = useState(null);

  const fetchCandidate = async () => {
    try {
      setLoading(true);
      const data = await candidateService.getCandidate(id);
      setCandidate(data);
      setError(null);
    } catch (err) {
      setError('Failed to load candidate');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCandidate();
  }, [id]);

  const handleRequestDocuments = async () => {
    try {
      setRequesting(true);
      const result = await candidateService.requestDocuments(id);
      setRequestResult(result);
      await fetchCandidate();
    } catch (err) {
      alert('Failed to request documents: ' + (err.response?.data?.error || err.message));
    } finally {
      setRequesting(false);
    }
  };

  const handleSubmitDocuments = async () => {
    if (!panFile && !aadhaarFile) {
      alert('Please select at least one document to upload');
      return;
    }

    try {
      setUploading(true);
      await candidateService.submitDocuments(id, panFile, aadhaarFile);
      alert('Documents uploaded successfully!');
      setPanFile(null);
      setAadhaarFile(null);
      await fetchCandidate();
    } catch (err) {
      alert('Failed to upload documents: ' + (err.response?.data?.error || err.message));
    } finally {
      setUploading(false);
    }
  };

  const getConfidenceColor = (score) => {
    if (score >= 0.8) return '#4CAF50';
    if (score >= 0.5) return '#FF9800';
    return '#f44336';
  };

  if (loading) {
    return <div className="loading-container">Loading candidate profile...</div>;
  }

  if (error || !candidate) {
    return (
      <div className="error-container">
        <p>{error || 'Candidate not found'}</p>
        <button onClick={() => navigate('/')}>Back to Dashboard</button>
      </div>
    );
  }

  return (
    <div className="candidate-profile">
      <div className="profile-header">
        <button className="back-button" onClick={() => navigate('/')}>
          ← Back to Dashboard
        </button>
        <h1>Candidate Profile</h1>
      </div>

      <div className="profile-content">
        {/* Basic Information */}
        <section className="profile-section">
          <h2>Basic Information</h2>
          <div className="info-grid">
            <div className="info-item">
              <label>Name</label>
              <div className="info-value">
                {candidate.name || 'N/A'}
                {candidate.confidence_scores?.name && (
                  <span
                    className="confidence-score"
                    style={{ color: getConfidenceColor(candidate.confidence_scores.name) }}
                  >
                    {(candidate.confidence_scores.name * 100).toFixed(0)}% confidence
                  </span>
                )}
              </div>
            </div>
            <div className="info-item">
              <label>Email</label>
              <div className="info-value">
                {candidate.email || 'N/A'}
                {candidate.confidence_scores?.email && (
                  <span
                    className="confidence-score"
                    style={{ color: getConfidenceColor(candidate.confidence_scores.email) }}
                  >
                    {(candidate.confidence_scores.email * 100).toFixed(0)}% confidence
                  </span>
                )}
              </div>
            </div>
            <div className="info-item">
              <label>Phone</label>
              <div className="info-value">
                {candidate.phone || 'N/A'}
                {candidate.confidence_scores?.phone && (
                  <span
                    className="confidence-score"
                    style={{ color: getConfidenceColor(candidate.confidence_scores.phone) }}
                  >
                    {(candidate.confidence_scores.phone * 100).toFixed(0)}% confidence
                  </span>
                )}
              </div>
            </div>
            <div className="info-item">
              <label>Company</label>
              <div className="info-value">
                {candidate.company || 'N/A'}
                {candidate.confidence_scores?.company && (
                  <span
                    className="confidence-score"
                    style={{ color: getConfidenceColor(candidate.confidence_scores.company) }}
                  >
                    {(candidate.confidence_scores.company * 100).toFixed(0)}% confidence
                  </span>
                )}
              </div>
            </div>
            <div className="info-item">
              <label>Designation</label>
              <div className="info-value">
                {candidate.designation || 'N/A'}
                {candidate.confidence_scores?.designation && (
                  <span
                    className="confidence-score"
                    style={{ color: getConfidenceColor(candidate.confidence_scores.designation) }}
                  >
                    {(candidate.confidence_scores.designation * 100).toFixed(0)}% confidence
                  </span>
                )}
              </div>
            </div>
            <div className="info-item">
              <label>Extraction Status</label>
              <div className="info-value">
                <span className={`status-badge status-${candidate.extraction_status}`}>
                  {candidate.extraction_status}
                </span>
              </div>
            </div>
          </div>
        </section>

        {/* Skills */}
        <section className="profile-section">
          <h2>Skills</h2>
          <div className="skills-container">
            {candidate.skills && candidate.skills.length > 0 ? (
              candidate.skills.map((skill, index) => (
                <span key={index} className="skill-tag">
                  {skill}
                </span>
              ))
            ) : (
              <p className="no-data">No skills extracted</p>
            )}
            {candidate.confidence_scores?.skills && (
              <span
                className="confidence-score"
                style={{ color: getConfidenceColor(candidate.confidence_scores.skills) }}
              >
                {(candidate.confidence_scores.skills * 100).toFixed(0)}% confidence
              </span>
            )}
          </div>
        </section>

        {/* Document Requests */}
        <section className="profile-section">
          <h2>Document Requests</h2>
          <button
            className="primary-button"
            onClick={handleRequestDocuments}
            disabled={requesting}
          >
            {requesting ? 'Generating Request...' : 'Request PAN & Aadhaar'}
          </button>

          {requestResult && (
            <div className="request-result">
              <h3>Generated Request ({requestResult.request.request_type})</h3>
              <div className="request-message">
                {requestResult.request.request_message}
              </div>
              {requestResult.agent_logs && requestResult.agent_logs.length > 0 && (
                <details className="agent-logs">
                  <summary>Agent Logs</summary>
                  <ul>
                    {requestResult.agent_logs.map((log, index) => (
                      <li key={index}>{log}</li>
                    ))}
                  </ul>
                </details>
              )}
            </div>
          )}

          {candidate.document_requests && candidate.document_requests.length > 0 && (
            <div className="previous-requests">
              <h3>Previous Requests</h3>
              {candidate.document_requests.map((req) => (
                <div key={req.id} className="request-item">
                  <div className="request-header">
                    <span className="request-type">{req.request_type}</span>
                    <span className="request-date">
                      {new Date(req.created_at).toLocaleString()}
                    </span>
                  </div>
                  <div className="request-preview">
                    {req.request_message.substring(0, 150)}...
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>

        {/* Upload Documents */}
        <section className="profile-section">
          <h2>Upload Documents</h2>
          <div className="document-upload">
            <div className="file-input-group">
              <label>PAN Card</label>
              <input
                type="file"
                accept=".pdf,.jpg,.jpeg,.png"
                onChange={(e) => setPanFile(e.target.files[0])}
              />
              {panFile && <span className="file-selected">{panFile.name}</span>}
            </div>
            <div className="file-input-group">
              <label>Aadhaar Card</label>
              <input
                type="file"
                accept=".pdf,.jpg,.jpeg,.png"
                onChange={(e) => setAadhaarFile(e.target.files[0])}
              />
              {aadhaarFile && <span className="file-selected">{aadhaarFile.name}</span>}
            </div>
            <button
              className="primary-button"
              onClick={handleSubmitDocuments}
              disabled={uploading || (!panFile && !aadhaarFile)}
            >
              {uploading ? 'Uploading...' : 'Submit Documents'}
            </button>
          </div>

          {candidate.documents && candidate.documents.length > 0 && (
            <div className="submitted-documents">
              <h3>Submitted Documents</h3>
              <div className="document-list">
                {candidate.documents.map((doc) => (
                  <div key={doc.id} className="document-item">
                    <span className="document-type">{doc.document_type.toUpperCase()}</span>
                    <span className="document-filename">{doc.filename}</span>
                    <span className="document-date">
                      {new Date(doc.uploaded_at).toLocaleDateString()}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </section>
      </div>
    </div>
  );
};

export default CandidateProfile;
