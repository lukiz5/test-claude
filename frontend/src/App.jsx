import { useState } from 'react'

const EXAMPLE_TEXT = `From: john@example.com
Subject: Meeting tomorrow
Don't forget about our meeting at 10 AM. We need to discuss the project timeline.

From: jane@example.com
Subject: Project update
Here's the latest status on the project. Everything is on track for the Q4 release.

From: mike@example.com
Subject: Budget approval needed
Please review and approve the budget proposal I sent yesterday.`

function App() {
  const [rawText, setRawText] = useState(EXAMPLE_TEXT)
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setSummary(null)

    try {
      if (!rawText.trim()) {
        throw new Error('Proszę wpisać tekst emaili.')
      }

      // Call backend API
      const response = await fetch('http://localhost:8000/summarize_raw', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: rawText }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to summarize emails')
      }

      const result = await response.json()
      setSummary(result)
    } catch (err) {
      setError(err.message || 'Wystąpił błąd podczas generowania podsumowania.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Email Summary
          </h1>
          <p className="text-gray-600">
            Wklej treść emaili lub notatki i wygeneruj inteligentne podsumowanie
          </p>
        </div>

        {/* Main Form */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label
                htmlFor="raw-text"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                Treść emaili
              </label>
              <textarea
                id="raw-text"
                rows={14}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
                value={rawText}
                onChange={(e) => setRawText(e.target.value)}
                placeholder="Wklej treść emaili lub notatki. Mogą być jeden pod drugim."
              />
              <p className="mt-2 text-xs text-gray-500">
                Możesz wkleić emaile skopiowane z Gmaila, Outlooka lub dowolne notatki tekstowe.
              </p>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-semibold py-3 px-4 rounded-md transition-colors duration-200 flex items-center justify-center"
            >
              {loading ? (
                <>
                  <svg
                    className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    ></circle>
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                  Generowanie podsumowania...
                </>
              ) : (
                'Generuj podsumowanie'
              )}
            </button>
          </form>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg
                  className="h-5 w-5 text-red-400"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                    clipRule="evenodd"
                  />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">Błąd</h3>
                <div className="mt-2 text-sm text-red-700">{error}</div>
              </div>
            </div>
          </div>
        )}

        {/* Summary Results */}
        {summary && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              Podsumowanie
            </h2>

            <div className="mb-6">
              <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wide mb-2">
                Streszczenie
              </h3>
              <p className="text-gray-800 leading-relaxed">{summary.summary}</p>
            </div>

            <div>
              <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wide mb-3">
                Najważniejsze zadania
              </h3>
              <ul className="space-y-2">
                {summary.top_actions.map((action, index) => (
                  <li key={index} className="flex items-start">
                    <span className="flex-shrink-0 h-6 w-6 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center text-sm font-semibold mr-3">
                      {index + 1}
                    </span>
                    <span className="text-gray-800 pt-0.5">{action}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
