'use client';

import React, { useState, useEffect } from 'react';
import { 
  Users, 
  Shield, 
  Building2, 
  User, 
  Radio, 
  Clock, 
  Activity,
  FileText,
  MapPin,
  AlertTriangle,
  CheckCircle,
  XCircle
} from 'lucide-react';

interface Unit {
  unit_id: string;
  name: string;
  parent_unit_id: string | null;
  level: string;
  created_at: string;
}

interface Soldier {
  soldier_id: string;
  name: string;
  rank: string;
  unit_id: string;
  device_id: string;
  status: string;
  created_at: string;
  last_seen: string;
}

interface RawInput {
  input_id: string;
  soldier_id: string;
  timestamp: string;
  raw_text: string;
  raw_audio_ref?: string;
  input_type: string;
  confidence: number;
  location_ref?: string;
  created_at: string;
}

interface Report {
  report_id: string;
  soldier_id: string;
  unit_id: string;
  timestamp: string;
  report_type: string;
  structured_json: string;
  confidence: number;
  source_input_id?: string;
  status: string;
  reviewed_by?: string;
  reviewed_at?: string;
  created_at: string;
  soldier_name?: string;
  unit_name?: string;
}

type SelectedNode = Unit & { soldiers?: Soldier[] } | Soldier;

interface DetailPanelProps {
  selectedNode: SelectedNode | null;
}

export function DetailPanel({ selectedNode }: DetailPanelProps) {
  const [rawInputs, setRawInputs] = useState<RawInput[]>([]);
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<'overview' | 'inputs' | 'reports'>('overview');

  useEffect(() => {
    if (selectedNode) {
      fetchNodeData();
    }
  }, [selectedNode]);

  const fetchNodeData = async () => {
    if (!selectedNode) return;

    setLoading(true);
    try {
      // Check if it's a soldier (has soldier_id) or a unit
      if ('soldier_id' in selectedNode) {
        // Fetch soldier-specific data
        const [inputsResponse, reportsResponse] = await Promise.all([
          fetch(`http://localhost:8000/soldiers/${selectedNode.soldier_id}/raw_inputs`),
          fetch(`http://localhost:8000/soldiers/${selectedNode.soldier_id}/reports`)
        ]);

        const inputsData = await inputsResponse.json();
        const reportsData = await reportsResponse.json();

        setRawInputs(inputsData.raw_inputs || []);
        setReports(reportsData.reports || []);
      } else {
        // For units, fetch all reports from soldiers in that unit
        const response = await fetch(`http://localhost:8000/units/${selectedNode.unit_id}/soldiers`);
        const soldiersData = await response.json();
        
        if (soldiersData.soldiers && soldiersData.soldiers.length > 0) {
          // Fetch reports for all soldiers in the unit
          const reportPromises = soldiersData.soldiers.map((soldier: any) =>
            fetch(`http://localhost:8000/soldiers/${soldier.soldier_id}/reports`)
          );
          
          const reportResponses = await Promise.all(reportPromises);
          const allReports = [];
          
          for (const res of reportResponses) {
            const data = await res.json();
            allReports.push(...(data.reports || []));
          }
          
          setReports(allReports);
          setRawInputs([]); // Units don't have direct raw inputs
        }
      }
    } catch (error) {
      console.error('Error fetching node data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getNodeIcon = (node: SelectedNode) => {
    if ('soldier_id' in node) {
      return <User className="h-5 w-5 text-blue-500" />;
    } else {
      switch (node.level.toLowerCase()) {
        case 'battalion':
          return <Building2 className="h-5 w-5 text-blue-500" />;
        case 'company':
          return <Shield className="h-5 w-5 text-green-500" />;
        case 'platoon':
          return <Users className="h-5 w-5 text-orange-500" />;
        case 'squad':
          return <User className="h-5 w-5 text-purple-500" />;
        default:
          return <Users className="h-5 w-5 text-gray-500" />;
      }
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status.toLowerCase()) {
      case 'active':
        return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'injured':
        return <AlertTriangle className="h-4 w-4 text-red-500" />;
      case 'missing':
        return <XCircle className="h-4 w-4 text-red-500" />;
      default:
        return <Activity className="h-4 w-4 text-gray-500" />;
    }
  };

  const getReportTypeColor = (type: string) => {
    switch (type) {
      case 'CASEVAC':
      case 'MEDEVAC':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'EOINCREP':
      case 'SPOTREP':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'INTREP':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'SITREP':
        return 'bg-green-100 text-green-800 border-green-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString();
  };

  if (!selectedNode) {
    return (
      <div className="h-full flex items-center justify-center bg-gray-50">
        <div className="text-center text-gray-500">
          <Users className="h-12 w-12 mx-auto mb-2 text-gray-300" />
          <p>Select a unit or soldier to view details</p>
        </div>
      </div>
    );
  }

  const isSoldier = 'soldier_id' in selectedNode;

  return (
    <div className="h-full flex flex-col bg-white">
      {/* Header */}
      <div className="p-4 border-b bg-gray-50">
        <div className="flex items-center gap-3">
          {getNodeIcon(selectedNode)}
          <div>
            <h2 className="text-lg font-semibold text-gray-800">
              {selectedNode.name}
            </h2>
            <p className="text-sm text-gray-600">
              {isSoldier ? selectedNode.rank : selectedNode.level}
            </p>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b">
        <button
          className={`px-4 py-2 text-sm font-medium ${
            activeTab === 'overview'
              ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50'
              : 'text-gray-500 hover:text-gray-700'
          }`}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button
          className={`px-4 py-2 text-sm font-medium ${
            activeTab === 'inputs'
              ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50'
              : 'text-gray-500 hover:text-gray-700'
          }`}
          onClick={() => setActiveTab('inputs')}
        >
          Raw Inputs ({rawInputs.length})
        </button>
        <button
          className={`px-4 py-2 text-sm font-medium ${
            activeTab === 'reports'
              ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50'
              : 'text-gray-500 hover:text-gray-700'
          }`}
          onClick={() => setActiveTab('reports')}
        >
          Reports ({reports.length})
        </button>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto">
        {loading ? (
          <div className="flex items-center justify-center h-32">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
          </div>
        ) : (
          <div className="p-4">
            {activeTab === 'overview' && (
              <div className="space-y-4">
                {/* Basic Info */}
                <div className="bg-gray-50 rounded-lg p-4">
                  <h3 className="font-medium text-gray-800 mb-3">Basic Information</h3>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-600">ID:</span>
                      <span className="font-mono">{isSoldier ? selectedNode.soldier_id : selectedNode.unit_id}</span>
                    </div>
                    {isSoldier && (
                      <>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Device:</span>
                          <span className="font-mono">{selectedNode.device_id}</span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-gray-600">Status:</span>
                          <div className="flex items-center gap-1">
                            {getStatusIcon(selectedNode.status)}
                            <span className="capitalize">{selectedNode.status}</span>
                          </div>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Last Seen:</span>
                          <span>{formatTimestamp(selectedNode.last_seen)}</span>
                        </div>
                      </>
                    )}
                    <div className="flex justify-between">
                      <span className="text-gray-600">Created:</span>
                      <span>{formatTimestamp(selectedNode.created_at)}</span>
                    </div>
                  </div>
                </div>

                {/* Statistics */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-blue-50 rounded-lg p-4">
                    <div className="flex items-center gap-2 mb-1">
                      <FileText className="h-4 w-4 text-blue-500" />
                      <span className="text-sm font-medium text-blue-700">Reports</span>
                    </div>
                    <div className="text-2xl font-bold text-blue-800">{reports.length}</div>
                  </div>
                  
                  {isSoldier && (
                    <div className="bg-green-50 rounded-lg p-4">
                      <div className="flex items-center gap-2 mb-1">
                        <Radio className="h-4 w-4 text-green-500" />
                        <span className="text-sm font-medium text-green-700">Inputs</span>
                      </div>
                      <div className="text-2xl font-bold text-green-800">{rawInputs.length}</div>
                    </div>
                  )}
                </div>

                {/* Recent Activity */}
                {reports.length > 0 && (
                  <div className="bg-gray-50 rounded-lg p-4">
                    <h3 className="font-medium text-gray-800 mb-3">Recent Activity</h3>
                    <div className="space-y-2">
                      {reports.slice(0, 3).map((report) => (
                        <div key={report.report_id} className="flex items-center gap-3 p-2 bg-white rounded">
                          <span className={`px-2 py-1 text-xs rounded border ${getReportTypeColor(report.report_type)}`}>
                            {report.report_type}
                          </span>
                          <span className="text-sm text-gray-600 flex-1 truncate">
                            {report.soldier_name || 'Unknown'}
                          </span>
                          <span className="text-xs text-gray-500">
                            {formatTimestamp(report.timestamp)}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'inputs' && (
              <div className="space-y-3">
                {rawInputs.length === 0 ? (
                  <div className="text-center py-8 text-gray-500">
                    <Radio className="h-12 w-12 mx-auto mb-2 text-gray-300" />
                    <p>No raw inputs available</p>
                  </div>
                ) : (
                  rawInputs.map((input) => (
                    <div key={input.input_id} className="border rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm font-medium text-gray-700">
                          {input.input_type.toUpperCase()}
                        </span>
                        <span className="text-xs text-gray-500">
                          {formatTimestamp(input.timestamp)}
                        </span>
                      </div>
                      <p className="text-sm text-gray-800 mb-2">{input.raw_text}</p>
                      <div className="flex items-center justify-between text-xs text-gray-500">
                        <span>Confidence: {(input.confidence * 100).toFixed(0)}%</span>
                        {input.location_ref && (
                          <span className="flex items-center gap-1">
                            <MapPin className="h-3 w-3" />
                            {input.location_ref}
                          </span>
                        )}
                      </div>
                    </div>
                  ))
                )}
              </div>
            )}

            {activeTab === 'reports' && (
              <div className="space-y-3">
                {reports.length === 0 ? (
                  <div className="text-center py-8 text-gray-500">
                    <FileText className="h-12 w-12 mx-auto mb-2 text-gray-300" />
                    <p>No reports available</p>
                  </div>
                ) : (
                  reports.map((report) => (
                    <div key={report.report_id} className="border rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <span className={`px-2 py-1 text-xs rounded border font-medium ${getReportTypeColor(report.report_type)}`}>
                          {report.report_type}
                        </span>
                        <span className="text-xs text-gray-500">
                          {formatTimestamp(report.timestamp)}
                        </span>
                      </div>
                      <div className="text-sm text-gray-600 mb-2">
                        <span className="font-medium">Soldier:</span> {report.soldier_name}
                      </div>
                      <div className="text-sm text-gray-600 mb-3">
                        <span className="font-medium">Confidence:</span> {(report.confidence * 100).toFixed(0)}%
                      </div>
                      <div className="bg-gray-50 rounded p-3">
                        <pre className="text-xs text-gray-800 whitespace-pre-wrap">
                          {JSON.stringify(JSON.parse(report.structured_json), null, 2)}
                        </pre>
                      </div>
                    </div>
                  ))
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
