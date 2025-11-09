import { useState } from 'react'
import FileUpload from '../components/FileUpload'
import { UploadResponse } from '../utils/api'
import { CheckCircle, AlertCircle } from 'lucide-react'
import { api } from '../utils/api'

export default function Home() {
  const [uploadResponse, setUploadResponse] = useState<UploadResponse | null>(null)
  const [ingesting, setIngesting] = useState(false)
  const [ingestStatus, setIngestStatus] = useState<'idle' | 'success' | 'error'>('idle')
  const [ingestMessage, setIngestMessage] = useState('')

  const handleUploadSuccess = async (response: UploadResponse) => {
    setUploadResponse(response)
    setIngestStatus('idle')
    setIngestMessage('')

    // Automatically trigger ingestion
    setIngesting(true)
    try {
      const ingestResponse = await api.ingestFile(response.file_id)
      setIngestStatus('success')
      setIngestMessage(
        `Document ingested successfully! ${ingestResponse.chunks_processed} chunks processed.`
      )
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || error.message || 'Ingestion failed'
      setIngestStatus('error')
      setIngestMessage(errorMessage)
    } finally {
      setIngesting(false)
    }
  }

  const handleUploadError = (error: string) => {
    console.error('Upload error:', error)
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">Welcome to RAGLedger</h1>
        <p className="text-lg text-gray-600">
          Upload banking documents and query them using AI-powered retrieval
        </p>
      </div>

      <div className="mb-8">
        <FileUpload onUploadSuccess={handleUploadSuccess} onUploadError={handleUploadError} />
      </div>

      {ingesting && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
          <div className="flex items-center space-x-2 text-blue-800">
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
            <span>Processing and ingesting document...</span>
          </div>
        </div>
      )}

      {ingestStatus !== 'idle' && ingestMessage && (
        <div
          className={`rounded-lg p-4 mb-4 flex items-center space-x-2 ${
            ingestStatus === 'success'
              ? 'bg-green-50 border border-green-200 text-green-800'
              : 'bg-red-50 border border-red-200 text-red-800'
          }`}
        >
          {ingestStatus === 'success' ? (
            <CheckCircle className="w-5 h-5" />
          ) : (
            <AlertCircle className="w-5 h-5" />
          )}
          <span>{ingestMessage}</span>
        </div>
      )}

      {uploadResponse && ingestStatus === 'success' && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4 text-gray-800">Next Steps</h2>
          <p className="text-gray-600 mb-4">
            Your document has been uploaded and processed. You can now query it using the Query
            page.
          </p>
          <a
            href="/query"
            className="inline-block bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 transition-colors"
          >
            Go to Query Page
          </a>
        </div>
      )}
    </div>
  )
}

