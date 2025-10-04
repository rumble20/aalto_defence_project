'use client';

import { useState } from 'react';
import { MilitaryHierarchyTree } from '@/components/military-hierarchy-tree';
import { DetailPanel } from '@/components/detail-panel';
import { Shield, Users, Activity } from 'lucide-react';

export default function Home() {
  const [selectedNode, setSelectedNode] = useState<any>(null);

  const handleNodeSelect = (node: any) => {
    setSelectedNode(node);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-gradient-to-r from-green-800 to-green-700 text-white shadow-lg">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Shield className="h-8 w-8" />
              <div>
                <h1 className="text-2xl font-bold">Military Command Dashboard</h1>
                <p className="text-green-200 text-sm">Hierarchical battlefield intelligence system</p>
              </div>
            </div>
            <div className="flex items-center gap-2 text-sm">
              <Activity className="h-4 w-4" />
              <span>Live System</span>
              <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex h-[calc(100vh-80px)]">
        {/* Left Sidebar - Hierarchy Tree */}
        <div className="w-1/3 border-r bg-white shadow-sm">
          <MilitaryHierarchyTree 
            onNodeSelect={handleNodeSelect}
            selectedNodeId={selectedNode?.unit_id || selectedNode?.soldier_id}
          />
        </div>

        {/* Right Panel - Details */}
        <div className="flex-1 bg-white">
          <DetailPanel selectedNode={selectedNode} />
        </div>
      </div>
    </div>
  );
}