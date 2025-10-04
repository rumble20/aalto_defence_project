"use client";

import { useState, useEffect } from "react";
import axios from "axios";
import { HierarchyTree, type TreeNode } from "@/components/hierarchy-tree";
import { AIChat } from "@/components/ai-chat";
import { NodeReports } from "@/components/node-reports";
import { StreamPanel } from "@/components/stream-panel";
import { DataStreamSelector } from "@/components/data-stream-selector";
import { ReportDrawer } from "@/components/report-drawer";
import { SummaryModal } from "@/components/summary-modal";
import { FRAGOBuilder } from "./components/frago-builder";
import {
  Shield,
  Users,
  Layers,
  FileBarChart,
  Radio,
  FileText,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

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
  const [selectedSoldier, setSelectedSoldier] = useState<string>("");
  const [rawInputs, setRawInputs] = useState<RawInput[]>([]);
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedUnit, setSelectedUnit] = useState("battalion");
  const [selectedItem, setSelectedItem] = useState<any>(null);
  const [showSummaryModal, setShowSummaryModal] = useState(false);
  const [showFRAGOBuilder, setShowFRAGOBuilder] = useState(false);

  // New state for hierarchy tree and node selection
  const [selectedNode, setSelectedNode] = useState<TreeNode | null>(null);
  const [nodeReports, setNodeReports] = useState<Report[]>([]);
  const [loadingNodeReports, setLoadingNodeReports] = useState(false);

  const API_BASE = "http://localhost:8000";

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
      console.error("Error fetching soldiers:", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchSoldierData = async (soldierId: string) => {
    try {
      const [rawResponse, reportsResponse] = await Promise.all([
        axios.get(`${API_BASE}/soldiers/${soldierId}/raw_inputs`),
        axios.get(`${API_BASE}/soldiers/${soldierId}/reports`),
      ]);

      setRawInputs(rawResponse.data.raw_inputs);
      setReports(reportsResponse.data.reports);
    } catch (error) {
      console.error("Error fetching soldier data:", error);
    }
  };

  // Helper function to recursively collect all soldier IDs from a unit and its subunits
  const collectSoldierIds = (node: TreeNode): string[] => {
    let soldierIds: string[] = [];

    // Add soldiers directly in this unit
    if (node.soldiers) {
      soldierIds.push(...node.soldiers.map((s: any) => s.soldier_id));
    }

    // Recursively add soldiers from subunits
    if (node.subunits) {
      for (const subunit of node.subunits) {
        // Convert Unit to TreeNode-like structure for recursion
        const subunitNode: TreeNode = {
          id: subunit.unit_id,
          name: subunit.name,
          type: "unit",
          unit_id: subunit.unit_id,
          soldiers: subunit.soldiers,
          subunits: subunit.subunits,
        };
        soldierIds.push(...collectSoldierIds(subunitNode));
      }
    }

    return soldierIds;
  };

  // Fetch reports for selected node (soldier or unit with subordinates)
  const fetchNodeReports = async (node: TreeNode) => {
    setLoadingNodeReports(true);
    try {
      let allReports: Report[] = [];

      if (node.type === "soldier") {
        // Fetch reports for single soldier
        const response = await axios.get(
          `${API_BASE}/soldiers/${node.soldier_id}/reports`
        );
        allReports = response.data.reports || [];
      } else if (node.type === "unit") {
        // Collect all soldier IDs from this unit and its subordinate units
        const soldierIds = collectSoldierIds(node);

        // Fetch all reports and filter by soldier IDs
        const response = await axios.get(`${API_BASE}/reports?limit=500`);
        const allAvailableReports = response.data.reports || [];

        // Filter reports that belong to soldiers in this unit hierarchy
        allReports = allAvailableReports.filter((report: Report) =>
          soldierIds.includes(report.soldier_id)
        );
      }

      setNodeReports(allReports);
    } catch (error) {
      console.error("Error fetching node reports:", error);
      setNodeReports([]);
    } finally {
      setLoadingNodeReports(false);
    }
  };

  // Handle node selection from hierarchy tree
  const handleNodeSelect = (node: TreeNode) => {
    setSelectedNode(node);
    fetchNodeReports(node);
  };

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString();
  };

  const getReportTypeColor = (type: string) => {
    const colors: { [key: string]: string } = {
      CASEVAC: "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300",
      EOINCREP:
        "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300",
      SITREP:
        "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300",
      FRAGO:
        "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300",
      OPORD:
        "bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300",
    };
    return (
      colors[type] ||
      "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300"
    );
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-xl text-foreground">
          Loading military dashboard...
        </div>
      </div>
    );
  }

  return (
    <div className="dark min-h-screen bg-background grid-background">
      <div className="container mx-auto p-3 space-y-3">
        <header className="flex items-center justify-between bg-card/50 backdrop-blur-sm p-3 rounded-lg neumorphic">
          <div>
            <h1 className="text-2xl font-bold tracking-tight font-mono text-foreground">
              TACTICAL OPS DASHBOARD
            </h1>
            <p className="text-xs text-muted-foreground mt-1">
              Real-time battlefield reporting and soldier monitoring
            </p>
          </div>

          <div className="flex items-center gap-2">
            <Button
              onClick={() => setShowFRAGOBuilder(!showFRAGOBuilder)}
              disabled={!selectedNode}
              className="bg-foreground/10 hover:bg-foreground/20 text-foreground font-mono border border-border h-8 text-xs"
              size="sm"
            >
              <FileText className="h-3 w-3 mr-1" />
              FRAGO
            </Button>
            <Button
              onClick={() => setShowSummaryModal(true)}
              className="bg-foreground/10 hover:bg-foreground/20 text-foreground font-mono border border-border h-8 text-xs"
              size="sm"
            >
              <FileBarChart className="h-3 w-3 mr-1" />
              SUMMARY
            </Button>
            <DataStreamSelector
              streams={unitLevels}
              selectedStream={selectedUnit}
              onStreamChange={setSelectedUnit}
            />
          </div>
        </header>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-3">
          {/* Left: Hierarchy Tree */}
          <div className="lg:col-span-1 h-[calc(100vh-140px)]">
            <HierarchyTree
              onNodeSelect={handleNodeSelect}
              selectedNodeId={selectedNode?.id}
            />
          </div>

          {/* Right: Split between Chat/FRAGO and Reports */}
          <div className="lg:col-span-3 grid grid-cols-1 lg:grid-cols-2 gap-3">
            {/* AI Chat or FRAGO Builder */}
            <div className="h-[calc(100vh-140px)]">
              {showFRAGOBuilder && selectedNode ? (
                <FRAGOBuilder
                  unitId={selectedNode.unit_id || selectedNode.id}
                  unitName={selectedNode.name}
                  soldierIds={collectSoldierIds(selectedNode)}
                  reports={nodeReports}
                />
              ) : (
                <AIChat selectedNode={selectedNode} reports={nodeReports} />
              )}
            </div>

            {/* Node Reports */}
            <div className="h-[calc(100vh-140px)]">
              <NodeReports
                selectedNode={selectedNode}
                reports={nodeReports}
                loading={loadingNodeReports}
                onReportClick={setSelectedItem}
              />
            </div>
          </div>
        </div>
      </div>

      <ReportDrawer
        selectedItem={selectedItem}
        onClose={() => setSelectedItem(null)}
      />
      <SummaryModal
        isOpen={showSummaryModal}
        onClose={() => setShowSummaryModal(false)}
      />
    </div>
  );
}
