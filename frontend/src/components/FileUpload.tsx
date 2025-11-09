import { useState } from 'react'
import { Upload, File, CheckCircle, AlertCircle, Loader } from 'lucide-react'
import { api, UploadResponse } from '../utils/api'

interface FileUploadProps {
  onUploadSuccess?: (response: UploadResponse) => void
  onUploadError?: (error: string) => void
}

export default function FileUpload({ onUploadSuccess, onUploadError }: FileUploadProps) {
  const [file, setFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'success' | 'error'>('idle')
  const [message, setMessage] = useState('')

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0]
      // Validate file type
      const validTypes = ['application/pdf', 'text/csv', 'application/vnd.ms-excel']
      if (validTypes.includes(selectedFile.type) || selectedFile.name.endsWith('.pdf') || selectedFile.name.endsWith('.csv')) {
        setFile(selectedFile)
        setUploadStatus('idle')
        setMessage('')
      } else {
        setMessage('Please upload a PDF or CSV file')
        setUploadStatus('error')
      }
    }
  }

  const handleUpload = async () => {
    if (!file) {
      setMessage('Please select a file first')
      setUploadStatus('error')
      return
    }

    setUploading(true)
    setUploadStatus('idle')
    setMessage('')

    try {
      const response = await api.uploadFile(file)
      setUploadStatus('success')
      setMessage(`File "${response.filename}" uploaded successfully! File ID: ${response.file_id}`)
      onUploadSuccess?.(response)
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || error.message || 'Upload failed'
      setMessage(errorMessage)
      setUploadStatus('error')
      onUploadError?.(errorMessage)
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-semibold mb-4 text-gray-800">Upload Document</h2>
      <div className="space-y-4">
        <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 hover:border-primary-400 transition-colors">
          <input
            type="file"
            id="file-upload"
            accept=".pdf,.csv"
            onChange={handleFileChange}
            className="hidden"
          />
          <label
            htmlFor="file-upload"
            className="cursor-pointer flex flex-col items-center justify-center"
          >
            <Upload className="w-12 h-12 text-gray-400 mb-2" />
            <span className="text-sm text-gray-600">
              {file ? file.name : 'Click to select PDF or CSV file'}
            </span>
          </label>
        </div>

        {file && (
          <div className="flex items-center space-x-2 text-sm text-gray-600">
            <File className="w-4 h-4" />
            <span>{file.name}</span>
            <span className="text-gray-400">({(file.size / 1024 / 1024).toFixed(2)} MB)</span>
          </div>
        )}

        <button
          onClick={handleUpload}
          disabled={!file || uploading}
          className="w-full bg-primary-600 text-white py-2 px-4 rounded-lg hover:bg-primary-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
        >
          {uploading ? (
            <>
              <Loader className="w-4 h-4 animate-spin" />
              <span>Uploading...</span>
            </>
          ) : (
            <>
              <Upload className="w-4 h-4" />
              <span>Upload File</span>
            </>
          )}
        </button>

        {message && (
          <div
            className={`flex items-center space-x-2 p-3 rounded-lg ${
              uploadStatus === 'success'
                ? 'bg-green-50 text-green-800'
                : uploadStatus === 'error'
                ? 'bg-red-50 text-red-800'
                : 'bg-blue-50 text-blue-800'
            }`}
          >
            {uploadStatus === 'success' && <CheckCircle className="w-5 h-5" />}
            {uploadStatus === 'error' && <AlertCircle className="w-5 h-5" />}
            <span className="text-sm">{message}</span>
          </div>
        )}
      </div>
    </div>
  )
}

