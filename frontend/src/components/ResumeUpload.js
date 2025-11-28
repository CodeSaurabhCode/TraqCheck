import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { candidateService } from '../services/api';
import './ResumeUpload.css';

const ResumeUpload = ({ onUploadSuccess }) => {
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState(null);

  const onDrop = useCallback(async (acceptedFiles) => {
    if (acceptedFiles.length === 0) return;

    const file = acceptedFiles[0];
    setUploading(true);
    setError(null);
    setUploadProgress(0);

    try {
      const result = await candidateService.uploadResume(file, (progressEvent) => {
        const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        setUploadProgress(progress);
      });

      setUploading(false);
      setUploadProgress(0);
      if (onUploadSuccess) {
        onUploadSuccess(result.candidate);
      }
    } catch (err) {
      setUploading(false);
      setUploadProgress(0);
      setError(err.response?.data?.error || 'Failed to upload resume');
    }
  }, [onUploadSuccess]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    },
    maxFiles: 1,
    disabled: uploading,
  });

  return (
    <div className="resume-upload">
      <div
        {...getRootProps()}
        className={`dropzone ${isDragActive ? 'active' : ''} ${uploading ? 'uploading' : ''}`}
      >
        <input {...getInputProps()} />
        {uploading ? (
          <div className="upload-progress">
            <div className="progress-bar">
              <div className="progress-fill" style={{ width: `${uploadProgress}%` }}></div>
            </div>
            <p>Uploading and parsing... {uploadProgress}%</p>
          </div>
        ) : isDragActive ? (
          <p>Drop the resume here...</p>
        ) : (
          <div className="upload-prompt">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <polyline points="17 8 12 3 7 8" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <line x1="12" y1="3" x2="12" y2="15" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            <p>Drag & drop a resume here, or click to select</p>
            <span className="file-types">PDF or DOCX (max 16MB)</span>
          </div>
        )}
      </div>
      {error && <div className="error-message">{error}</div>}
    </div>
  );
};

export default ResumeUpload;
