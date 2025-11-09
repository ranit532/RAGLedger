import { FileText, TrendingUp, ExternalLink } from 'lucide-react'
import { Source } from '../utils/api'

interface ResultsViewProps {
  answer: string
  sources: Source[]
  query: string
}

export default function ResultsView({ answer, sources, query }: ResultsViewProps) {
  const getScoreColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600 bg-green-50'
    if (score >= 0.6) return 'text-yellow-600 bg-yellow-50'
    return 'text-red-600 bg-red-50'
  }

  return (
    <div className="space-y-6">
      {/* Query */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-sm font-semibold text-gray-500 mb-2">Your Question</h3>
        <p className="text-lg text-gray-800">{query}</p>
      </div>

      {/* Answer */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Answer</h3>
        <div className="prose max-w-none">
          <p className="text-gray-700 whitespace-pre-wrap">{answer}</p>
        </div>
      </div>

      {/* Sources */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
          <FileText className="w-5 h-5 mr-2" />
          Sources ({sources.length})
        </h3>
        <div className="space-y-4">
          {sources.map((source, index) => (
            <div
              key={source.chunk_id || index}
              className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center space-x-2">
                  <span className="text-sm font-medium text-gray-700">{source.filename}</span>
                  {source.page && (
                    <span className="text-xs text-gray-500">Page {source.page}</span>
                  )}
                </div>
                <div
                  className={`px-2 py-1 rounded text-xs font-semibold ${getScoreColor(
                    source.similarity_score
                  )}`}
                >
                  <TrendingUp className="w-3 h-3 inline mr-1" />
                  {(source.similarity_score * 100).toFixed(1)}%
                </div>
              </div>
              <p className="text-sm text-gray-600 line-clamp-3">{source.content}</p>
              {source.metadata && Object.keys(source.metadata).length > 0 && (
                <div className="mt-2 pt-2 border-t border-gray-100">
                  <div className="flex flex-wrap gap-2">
                    {Object.entries(source.metadata).map(([key, value]) => (
                      <span
                        key={key}
                        className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded"
                      >
                        {key}: {String(value)}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

