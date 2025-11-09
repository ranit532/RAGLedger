import { useState } from 'react'
import SearchBox from '../components/SearchBox'
import ResultsView from '../components/ResultsView'
import { api, QueryResponse } from '../utils/api'
import { AlertCircle } from 'lucide-react'

export default function Query() {
  const [queryResponse, setQueryResponse] = useState<QueryResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSearch = async (query: string) => {
    setLoading(true)
    setError(null)
    setQueryResponse(null)

    try {
      const response = await api.query(query, 5)
      setQueryResponse(response)
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.message || 'Query failed'
      setError(errorMessage)
      console.error('Query error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">Query Documents</h1>
        <p className="text-lg text-gray-600">
          Ask questions about your uploaded banking documents
        </p>
      </div>

      <div className="mb-8">
        <SearchBox onSearch={handleSearch} loading={loading} />
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4 flex items-center space-x-2 text-red-800">
          <AlertCircle className="w-5 h-5" />
          <span>{error}</span>
        </div>
      )}

      {queryResponse && (
        <ResultsView
          answer={queryResponse.answer}
          sources={queryResponse.sources}
          query={queryResponse.query}
        />
      )}

      {!queryResponse && !loading && !error && (
        <div className="bg-white rounded-lg shadow-md p-12 text-center">
          <p className="text-gray-500 text-lg">
            Enter a question above to search through your documents
          </p>
        </div>
      )}
    </div>
  )
}

