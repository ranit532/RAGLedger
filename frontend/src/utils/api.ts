import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface UploadResponse {
  message: string
  file_id: string
  filename: string
}

export interface IngestResponse {
  message: string
  chunks_processed: number
}

export interface QueryResponse {
  answer: string
  sources: Source[]
  query: string
}

export interface Source {
  filename: string
  page?: number
  chunk_id: string
  similarity_score: number
  content: string
  metadata?: Record<string, any>
}

export interface HealthResponse {
  status: string
  version: string
  services: {
    openai: string
    pinecone: string
    s3: string
  }
}

export const api = {
  // Health check
  async health(): Promise<HealthResponse> {
    const response = await apiClient.get('/health')
    return response.data
  },

  // Upload file
  async uploadFile(file: File): Promise<UploadResponse> {
    const formData = new FormData()
    formData.append('file', file)
    const response = await apiClient.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  // Ingest file
  async ingestFile(fileId: string): Promise<IngestResponse> {
    const response = await apiClient.post('/ingest', { file_id: fileId })
    return response.data
  },

  // Query
  async query(question: string, topK: number = 5): Promise<QueryResponse> {
    const response = await apiClient.post('/query', {
      query: question,
      top_k: topK,
    })
    return response.data
  },
}

export default api

