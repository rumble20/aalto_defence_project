'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';

interface Soldier {
  soldier_id: string;
  name: string;
  rank: string;
  unit_id: string;
  device_id: string;
  unit_name: string;
  unit_level: string;
}

interface RawInput {
  input_id: string;
  soldier_id: string;
  timestamp: string;
  raw_text: string;
  raw_audio_ref?: string;
}

interface Report {
  report_id: string;
  soldier_id: string;
  unit_id: string;
  timestamp: string;
  report_type: string;
  structured_json: string;
  confidence: number;
  soldier_name: string;
  unit_name: string;
}

export default function Home() {
  const [soldiers, setSoldiers] = useState<Soldier[]>([]);
  const [selectedSoldier, setSelectedSoldier] = useState<string>('');
  const [rawInputs, setRawInputs] = useState<RawInput[]>([]);
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);

  const API_BASE = 'http://localhost:8000';

  useEffect(() => {
    fetchSoldiers();
  }, []);

  useEffect(() => {
    if (selectedSoldier) {
      fetchSoldierData(selectedSoldier);
    }
  }, [selectedSoldier]);

  const fetchSoldiers = async () => {
    try {
      const response = await axios.get(`${API_BASE}/soldiers`);
      setSoldiers(response.data.soldiers);
      if (response.data.soldiers.length > 0) {
        setSelectedSoldier(response.data.soldiers[0].soldier_id);
      }
    } catch (error) {
      console.error('Error fetching soldiers:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchSoldierData = async (soldierId: string) => {
    try {
      const [rawResponse, reportsResponse] = await Promise.all([
        axios.get(`${API_BASE}/soldiers/${soldierId}/raw_inputs`),
        axios.get(`${API_BASE}/soldiers/${soldierId}/reports`)
      ]);
      
      setRawInputs(rawResponse.data.raw_inputs);
      setReports(reportsResponse.data.reports);
    } catch (error) {
      console.error('Error fetching soldier data:', error);
    }
  };

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString();
  };

  const getReportTypeColor = (type: string) => {
    const colors: { [key: string]: string } = {
      'CASEVAC': 'bg-red-100 text-red-800',
      'EOINCREP': 'bg-yellow-100 text-yellow-800',
      'SITREP': 'bg-blue-100 text-blue-800',
      'FRAGO': 'bg-green-100 text-green-800',
      'OPORD': 'bg-purple-100 text-purple-800'
    };
    return colors[type] || 'bg-gray-100 text-gray-800';
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading military dashboard...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-green-800 text-white p-6">
        <h1 className="text-3xl font-bold">Military Command Dashboard</h1>
        <p className="text-green-200 mt-2">Real-time soldier communication monitoring</p>
      </header>

      <div className="container mx-auto p-6">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Soldier Selection Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold mb-4">Select Soldier</h2>
              <div className="space-y-2">
                {soldiers.map((soldier) => (
                  <button
                    key={soldier.soldier_id}
                    onClick={() => setSelectedSoldier(soldier.soldier_id)}
                    className={`w-full text-left p-3 rounded border transition-colors ${
                      selectedSoldier === soldier.soldier_id
                        ? 'bg-green-100 border-green-500 text-green-800'
                        : 'bg-gray-50 border-gray-200 hover:bg-gray-100'
                    }`}
                  >
                    <div className="font-medium">{soldier.name}</div>
                    <div className="text-sm text-gray-600">{soldier.rank}</div>
                    <div className="text-xs text-gray-500">{soldier.unit_name}</div>
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3">
            {selectedSoldier ? (
              <div className="space-y-6">
                {/* Raw Inputs */}
                <div className="bg-white rounded-lg shadow p-6">
                  <h2 className="text-xl font-semibold mb-4">Raw Voice Inputs</h2>
                  <div className="space-y-3 max-h-96 overflow-y-auto">
                    {rawInputs.length > 0 ? (
                      rawInputs.map((input) => (
                        <div key={input.input_id} className="border-l-4 border-blue-500 pl-4 py-2">
                          <div className="text-sm text-gray-600 mb-1">
                            {formatTimestamp(input.timestamp)}
                          </div>
                          <div className="text-gray-800">{input.raw_text}</div>
                        </div>
                      ))
                    ) : (
                      <div className="text-gray-500 italic">No raw inputs available</div>
                    )}
                  </div>
                </div>

                {/* Structured Reports */}
                <div className="bg-white rounded-lg shadow p-6">
                  <h2 className="text-xl font-semibold mb-4">AI-Generated Reports</h2>
                  <div className="space-y-4 max-h-96 overflow-y-auto">
                    {reports.length > 0 ? (
                      reports.map((report) => (
                        <div key={report.report_id} className="border rounded-lg p-4">
                          <div className="flex items-center justify-between mb-2">
                            <span className={`px-2 py-1 rounded text-xs font-medium ${getReportTypeColor(report.report_type)}`}>
                              {report.report_type}
                            </span>
                            <div className="text-sm text-gray-600">
                              {formatTimestamp(report.timestamp)}
                            </div>
                          </div>
                          <div className="text-sm text-gray-600 mb-2">
                            Confidence: {(report.confidence * 100).toFixed(0)}%
                          </div>
                          <div className="bg-gray-50 p-3 rounded text-sm">
                            <pre className="whitespace-pre-wrap text-xs">
                              {JSON.stringify(JSON.parse(report.structured_json), null, 2)}
                            </pre>
                          </div>
                        </div>
                      ))
                    ) : (
                      <div className="text-gray-500 italic">No structured reports available</div>
                    )}
                  </div>
                </div>
              </div>
            ) : (
              <div className="bg-white rounded-lg shadow p-6 text-center">
                <div className="text-gray-500">Select a soldier to view their data</div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}