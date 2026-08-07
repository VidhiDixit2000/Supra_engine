import axios from 'axios';

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
  timeout: 60000,
});

export const getUsers = async () => {
  const { data } = await apiClient.get('/users');
  return data;
};

export const getCandidateSet = async (userId) => {
  const { data } = await apiClient.get(`/candidate-set/${encodeURIComponent(userId)}`);
  return data;
};

export default apiClient;
