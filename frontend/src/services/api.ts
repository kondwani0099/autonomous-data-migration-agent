import axios from 'axios';
import { MigrationJob, Clarification, DataPreview } from '../types';

const API_BASE = '/api';

export const api = {
  async getJobs(): Promise<MigrationJob[]> {
    const res = await axios.get(`${API_BASE}/jobs`);
    return res.data;
  },

  async createJob(clientId: string, clientName: string): Promise<MigrationJob> {
    const res = await axios.post(`${API_BASE}/jobs`, {
      client_id: clientId,
      client_name: clientName,
    });
    return res.data;
  },

  async getJob(jobId: string): Promise<MigrationJob> {
    const res = await axios.get(`${API_BASE}/jobs/${jobId}`);
    return res.data;
  },

  async getClarifications(jobId: string): Promise<Clarification[]> {
    const res = await axios.get(`${API_BASE}/jobs/${jobId}/clarifications`);
    return res.data;
  },

  async answerClarification(clarificationId: string, answer: string): Promise<void> {
    await axios.post(`${API_BASE}/clarifications/${clarificationId}/answer`, { answer });
  },

  async getPreview(jobId: string): Promise<DataPreview> {
    const res = await axios.get(`${API_BASE}/jobs/${jobId}/preview`);
    return res.data;
  },

  async approveImport(jobId: string): Promise<void> {
    await axios.post(`${API_BASE}/jobs/${jobId}/approve`);
  },
};
