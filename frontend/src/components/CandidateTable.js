import React from 'react';
import { useNavigate } from 'react-router-dom';
import './CandidateTable.css';

const CandidateTable = ({ candidates }) => {
  const navigate = useNavigate();

  const getStatusBadge = (status) => {
    const statusClasses = {
      completed: 'status-completed',
      processing: 'status-processing',
      pending: 'status-pending',
      failed: 'status-failed',
    };
    return <span className={`status-badge ${statusClasses[status] || ''}`}>{status}</span>;
  };

  const handleRowClick = (id) => {
    navigate(`/candidate/${id}`);
  };

  if (!candidates || candidates.length === 0) {
    return (
      <div className="empty-state">
        <p>No candidates yet. Upload a resume to get started!</p>
      </div>
    );
  }

  return (
    <div className="candidate-table-container">
      <table className="candidate-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Company</th>
            <th>Designation</th>
            <th>Status</th>
            <th>Documents</th>
          </tr>
        </thead>
        <tbody>
          {candidates.map((candidate) => (
            <tr key={candidate.id} onClick={() => handleRowClick(candidate.id)} className="clickable-row">
              <td>{candidate.name || '-'}</td>
              <td>{candidate.email || '-'}</td>
              <td>{candidate.phone || '-'}</td>
              <td>{candidate.company || '-'}</td>
              <td>{candidate.designation || '-'}</td>
              <td>{getStatusBadge(candidate.extraction_status)}</td>
              <td>
                <div className="document-count">
                  {candidate.documents?.length || 0}/2
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CandidateTable;
