'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
import { StreamPanel } from '@/components/stream-panel';
import { DataStreamSelector } from '@/components/data-stream-selector';
import { ReportDrawer } from '@/components/report-drawer';
import { SummaryModal } from '@/components/summary-modal';
import { Shield, Users, Layers, FileBarChart, Radio } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';

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
  const [selectedUnit, setSelectedUnit] = useState("battalion");
  const [selectedItem, setSelectedItem] = useState<any>(null);
  const [showSummaryModal, setShowSummaryModal] = useState(false);

  const API_BASE = 'http://localhost:8000';

  const unitLevels = [
    { id: "brigade", name: "Brigade", icon: Layers },
    { id: "battalion", name: "Battalion", icon: Shield },
    { id: "company", name: "Company", icon: Users },
    { id: "platoon", name: "Platoon", icon: Users },
    { id: "squad", name: "Squad", icon: Users },
  ];

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
      'CASEVAC': 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300',
      'EOINCREP': 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300',
      'SITREP': 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300',
      'FRAGO': 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300',
      'OPORD': 'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300'
    };
    return colors[type] || 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300';
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-xl text-foreground">Loading military dashboard...</div>
      </div>
    );
  }

  return (
    <div className="dark min-h-screen bg-background grid-background">
      <div className="container mx-auto p-6 space-y-6">
        <header className="flex items-center justify-between bg-card/50 backdrop-blur-sm p-6 rounded-lg neumorphic">
          <div>
            <h1 className="text-4xl font-bold tracking-tight font-mono text-foreground">TACTICAL OPS DASHBOARD</h1>
            <p className="text-muted-foreground mt-2">Real-time battlefield reporting and soldier monitoring system</p>
          </div>

          <div className="flex items-center gap-3">
            <Button
              onClick={() => setShowSummaryModal(true)}
              className="bg-foreground/10 hover:bg-foreground/20 text-foreground font-mono border border-border"
            >
              <FileBarChart className="h-4 w-4 mr-2" />
              SUMMARIZE
            </Button>
            <DataStreamSelector streams={unitLevels} selectedStream={selectedUnit} onStreamChange={setSelectedUnit} />
          </div>
        </header>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Soldier Selection Sidebar */}
          <div className="lg:col-span-1">
            <Card className="neumorphic border-0 p-6">
              <h2 className="text-xl font-semibold mb-4 font-mono flex items-center gap-2 text-foreground">
                <Radio className="h-5 w-5" />
                ACTIVE UNITS
              </h2>
              <div className="space-y-2">
                {soldiers.map((soldier) => (
                  <button
                    key={soldier.soldier_id}
                    onClick={() => setSelectedSoldier(soldier.soldier_id)}
                    className={`w-full text-left p-3 rounded border transition-colors ${
                      selectedSoldier === soldier.soldier_id
                        ? 'bg-military-olive/20 border-military-olive/30 text-foreground'
                        : 'bg-muted/30 border-border hover:bg-muted/50 text-foreground'
                    }`}
                  >
                    <div className="font-medium">{soldier.name}</div>
                    <div className="text-sm text-muted-foreground">{soldier.rank}</div>
                    <div className="text-xs text-muted-foreground">{soldier.unit_name}</div>
                  </button>
                ))}
              </div>
            </Card>
          </div>

          {/* Main Content Area */}
          <div className="lg:col-span-3 space-y-6">
            {/* Live Reports Stream */}
            <StreamPanel streamId={selectedUnit} onItemClick={setSelectedItem} />

            {/* Soldier-Specific Data */}
            {selectedSoldier && (
              <div className="space-y-6">
                {/* Raw Inputs */}
                <Card className="neumorphic border-0 p-6">
                  <h2 className="text-xl font-semibold mb-4 font-mono text-foreground">Raw Voice Inputs</h2>
                  <div className="space-y-3 max-h-96 overflow-y-auto">
                    {rawInputs.length > 0 ? (
                      rawInputs.map((input) => (
                        <div key={input.input_id} className="border-l-4 border-military-blue pl-4 py-2 bg-muted/20 rounded">
                          <div className="text-sm text-muted-foreground mb-1 font-mono">
                            {formatTimestamp(input.timestamp)}
                          </div>
                          <div className="text-foreground">{input.raw_text}</div>
                        </div>
                      ))
                    ) : (
                      <div className="text-muted-foreground italic">No raw inputs available</div>
                    )}
                  </div>
                </Card>

                {/* Structured Reports */}
                <Card className="neumorphic border-0 p-6">
                  <h2 className="text-xl font-semibold mb-4 font-mono text-foreground">AI-Generated Reports</h2>
                  <div className="space-y-4 max-h-96 overflow-y-auto">
                    {reports.length > 0 ? (
                      reports.map((report) => (
                        <div key={report.report_id} className="border rounded-lg p-4 bg-muted/20 border-border">
                          <div className="flex items-center justify-between mb-2">
                            <span className={`px-2 py-1 rounded text-xs font-medium font-mono ${getReportTypeColor(report.report_type)}`}>
                              {report.report_type}
                            </span>
                            <div className="text-sm text-muted-foreground font-mono">
                              {formatTimestamp(report.timestamp)}
                            </div>
                          </div>
                          <div className="text-sm text-muted-foreground mb-2 font-mono">
                            Confidence: {(report.confidence * 100).toFixed(0)}%
                          </div>
                          <div className="bg-background/50 p-3 rounded text-sm">
                            <pre className="whitespace-pre-wrap text-xs text-foreground font-mono">
                              {JSON.stringify(JSON.parse(report.structured_json), null, 2)}
                            </pre>
                          </div>
                        </div>
                      ))
                    ) : (
                      <div className="text-muted-foreground italic">No structured reports available</div>
                    )}
                  </div>
                </Card>
              </div>
            )}
          </div>
        </div>
      </div>

      <ReportDrawer selectedItem={selectedItem} onClose={() => setSelectedItem(null)} />
      <SummaryModal isOpen={showSummaryModal} onClose={() => setShowSummaryModal(false)} />
    </div>
  );
}
