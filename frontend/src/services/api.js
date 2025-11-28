import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const candidateService = {
  // Upload resume
  uploadResume: async (file, onUploadProgress) => {
    const formData = new FormData();
    formData.append('resume', file);
    
    const response = await api.post('/candidates/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress,
    });
    return response.data;
  },

  // Get all candidates
  getCandidates: async () => {
    const response = await api.get('/candidates');
    return response.data;
  },

  // Get single candidate
  getCandidate: async (id) => {
    const response = await api.get(`/candidates/${id}`);
    return response.data;
  },

  // Request documents
  requestDocuments: async (id) => {
    const response = await api.post(`/candidates/${id}/request-documents`);
    return response.data;
  },

  // Submit documents
  submitDocuments: async (id, panFile, aadhaarFile) => {
    const formData = new FormData();
    if (panFile) formData.append('pan', panFile);
    if (aadhaarFile) formData.append('aadhaar', aadhaarFile);
    
    const response = await api.post(`/candidates/${id}/submit-documents`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};

export default api;
