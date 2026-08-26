import axios from 'axios';
import { MigrationJob, Clarification, DataPreview, AuditLogEntry, DataCategory, DataCategoryOption, DocumentItem } from '../types';

const API_BASE = '/api';

export interface UploadResult {
  document_id: string;
  file_name: string;
  file_type: string;
  status: string;
  message: string;
}

export const api = {
  async getJobs(): Promise<MigrationJob[]> {
    const res = await axios.get(`${API_BASE}/jobs`);
    return res.data;
  },

  async getDataCategories(): Promise<DataCategoryOption[]> {
    const res = await axios.get(`${API_BASE}/data-categories`);
    return res.data;
  },

  async getDocuments(jobId: string): Promise<DocumentItem[]> {
    const res = await axios.get(`${API_BASE}/jobs/${jobId}/documents`);
    return res.data;
  },

  async createJob(clientId: string, clientName: string, dataCategory: DataCategory = 'sales'): Promise<MigrationJob> {
    const res = await axios.post(`${API_BASE}/jobs`, {
      client_id: clientId,
      client_name: clientName,
      data_category: dataCategory,
    });
    return res.data;
  },

  async uploadFiles(jobId: string, files: File[]): Promise<UploadResult[]> {
    const formData = new FormData();
    for (const file of files) {
      formData.append('files', file);
    }
    const res = await axios.post(`${API_BASE}/jobs/${jobId}/upload`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
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
    await axios.post(`${API_BASE}/jobs/clarifications/${clarificationId}/answer`, { answer });
  },

  async getPreview(jobId: string): Promise<DataPreview> {
    const res = await axios.get(`${API_BASE}/jobs/${jobId}/preview`);
    return res.data;
  },

  async savePreviewRecords(jobId: string, records: Record<string, unknown>[]): Promise<DataPreview> {
    const res = await axios.post(`${API_BASE}/jobs/${jobId}/preview`, { records });
    return res.data;
  },

  async approveImport(jobId: string): Promise<void> {
    await axios.post(`${API_BASE}/jobs/${jobId}/approve`);
  },

  async getAuditTrail(jobId: string): Promise<AuditLogEntry[]> {
    const res = await axios.get(`${API_BASE}/jobs/${jobId}/audit`);
    return res.data;
  },
};
