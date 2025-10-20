'use client';

import { useState } from 'react';
import { Upload, FileText, Loader2 } from 'lucide-react';

interface ClassificationResult {
  verbPhrases: Array<{ label: string; firstWord: string }>;
  nounPhrases: Array<{ label: string; firstWord: string }>;
  others: Array<{ label: string; firstWord: string; wordType: string }>;
  skipped: string[];
  statistics: {
    total: number;
    actionCount: number;
    objectCount: number;
    unclassifiedCount: number;
    skippedCount: number;
  };
}

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ClassificationResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setResult(null);
      setError(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    setError(null);

    try {
      // Read file content
      const xmlContent = await file.text();

      // Extract labels
      const extractResponse = await fetch('/api/extract', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ xmlContent })
      });

      if (!extractResponse.ok) {
        throw new Error('Failed to extract labels');
      }

      const { labels } = await extractResponse.json();

      // Classify labels
      const classifyResponse = await fetch('/api/classify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ labels })
      });

      if (!classifyResponse.ok) {
        throw new Error('Failed to classify labels');
      }

      const classification = await classifyResponse.json();
      setResult(classification);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <div className="container mx-auto px-4 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-800 mb-4">
            BPE AI Analyzer
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Business Process Element Classification based on Grammatical Structure
          </p>
        </div>

        {/* Upload Section */}
        <div className="max-w-3xl mx-auto mb-12">
          <form onSubmit={handleSubmit} className="bg-white rounded-2xl shadow-xl p-8">
            <div className="mb-6">
              <label
                htmlFor="file-upload"
                className="flex flex-col items-center justify-center w-full h-64 border-2 border-dashed border-gray-300 rounded-xl cursor-pointer bg-gray-50 hover:bg-gray-100 transition-all"
              >
                <div className="flex flex-col items-center justify-center pt-5 pb-6">
                  {file ? (
                    <>
                      <FileText className="w-16 h-16 text-blue-500 mb-4" />
                      <p className="mb-2 text-lg font-semibold text-gray-700">
                        {file.name}
                      </p>
                      <p className="text-sm text-gray-500">
                        Click to change file
                      </p>
                    </>
                  ) : (
                    <>
                      <Upload className="w-16 h-16 text-gray-400 mb-4" />
                      <p className="mb-2 text-lg font-semibold text-gray-700">
                        Upload XML File
                      </p>
                      <p className="text-sm text-gray-500">
                        Click to browse or drag and drop
                      </p>
                    </>
                  )}
                </div>
                <input
                  id="file-upload"
                  type="file"
                  accept=".xml"
                  onChange={handleFileChange}
                  className="hidden"
                />
              </label>
            </div>

            <button
              type="submit"
              disabled={!file || loading}
              className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold py-4 px-6 rounded-xl hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl"
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <Loader2 className="animate-spin mr-2" />
                  Analyzing...
                </span>
              ) : (
                'Analyze Business Process'
              )}
            </button>
          </form>
        </div>

        {/* Error Message */}
        {error && (
          <div className="max-w-3xl mx-auto mb-8">
            <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded-lg">
              <p className="text-red-700 font-semibold">Error: {error}</p>
            </div>
          </div>
        )}

        {/* Results Section */}
        {result && (
          <div className="max-w-6xl mx-auto">
            {/* Statistics */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
              <StatCard
                title="Total Labels"
                value={result.statistics.total}
                color="blue"
              />
              <StatCard
                title="Action Phrases"
                value={result.statistics.actionCount}
                color="green"
              />
              <StatCard
                title="Object/State"
                value={result.statistics.objectCount}
                color="purple"
              />
              <StatCard
                title="Unclassified"
                value={result.statistics.unclassifiedCount}
                color="orange"
              />
            </div>

            {/* Verb Phrases */}
            <ResultSection
              title="Action Phrases (Verb-led)"
              count={result.verbPhrases.length}
              color="green"
              items={result.verbPhrases}
            />

            {/* Noun Phrases */}
            <ResultSection
              title="Object/State Phrases (Noun-led)"
              count={result.nounPhrases.length}
              color="purple"
              items={result.nounPhrases}
            />

            {/* Others */}
            {result.others.length > 0 && (
              <ResultSection
                title="Unclassified/Other"
                count={result.others.length}
                color="orange"
                items={result.others}
              />
            )}
          </div>
        )}
      </div>
    </div>
  );
}

function StatCard({ title, value, color }: { title: string; value: number; color: string }) {
  const colorClasses: Record<string, string> = {
    blue: 'from-blue-500 to-blue-600',
    green: 'from-green-500 to-green-600',
    purple: 'from-purple-500 to-purple-600',
    orange: 'from-orange-500 to-orange-600'
  };

  return (
    <div className={`bg-gradient-to-br ${colorClasses[color]} rounded-xl p-6 text-white shadow-lg`}>
      <h3 className="text-sm font-medium opacity-90 mb-2">{title}</h3>
      <p className="text-4xl font-bold">{value}</p>
    </div>
  );
}

function ResultSection({
  title,
  count,
  color,
  items
}: {
  title: string;
  count: number;
  color: string;
  items: Array<{ label: string; firstWord: string; wordType?: string }>;
}) {
  const borderClasses: Record<string, string> = {
    green: 'border-green-500',
    purple: 'border-purple-500',
    orange: 'border-orange-500'
  };

  return (
    <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
      <div className={`border-l-4 ${borderClasses[color]} pl-4 mb-6`}>
        <h2 className="text-2xl font-bold text-gray-800">
          {title} <span className="text-gray-500">({count} items)</span>
        </h2>
      </div>

      {items.length > 0 ? (
        <div className="space-y-3">
          {items.map((item, idx) => (
            <div
              key={idx}
              className="flex items-start justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <span className="text-gray-800 font-medium flex-1">
                {item.label}
              </span>
              <span className="text-sm text-gray-500 ml-4">
                starts with: <span className="font-semibold">{item.firstWord}</span>
                {item.wordType && ` (${item.wordType})`}
              </span>
            </div>
          ))}
        </div>
      ) : (
        <p className="text-gray-500 italic">No items found</p>
      )}
    </div>
  );
}
