'use client';

import { useState } from 'react';
import { MilitaryHierarchyTree } from '@/components/military-hierarchy-tree';
import { DetailPanel } from '@/components/detail-panel';
import { Shield, Users, Activity } from 'lucide-react';
import { cn } from '@/lib/utils';

export default function Home() {
  const [selectedNode, setSelectedNode] = useState<any>(null);

  const handleNodeSelect = (node: any) => {
    setSelectedNode(node);
  };

  return (
    <div className="dark min-h-screen bg-background grid-background">
      <div className="container mx-auto p-6 space-y-6">
        {/* Header */}
        <header className="flex items-center justify-between bg-card/50 backdrop-blur-sm p-6 rounded-lg neumorphic">
          <div className="flex items-center gap-3">
            <Shield className="h-8 w-8 text-foreground" />
            <div>
              <h1 className="text-4xl font-bold tracking-tight font-mono text-foreground">TACTICAL OPS</h1>
              <p className="text-muted-foreground mt-1">Live battlefield reporting system</p>
            </div>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <Activity className="h-4 w-4 text-foreground" />
            <span className="text-foreground font-mono">LIVE SYSTEM</span>
            <div className="w-2 h-2 bg-foreground rounded-full animate-pulse"></div>
          </div>
        </header>

        {/* Main Content */}
        <div className="flex gap-6 h-[calc(100vh-200px)]">
          {/* Left Sidebar - Hierarchy Tree */}
          <div className="w-1/3 neumorphic rounded-lg overflow-hidden">
            <MilitaryHierarchyTree 
              onNodeSelect={handleNodeSelect}
              selectedNodeId={selectedNode?.unit_id || selectedNode?.soldier_id}
            />
          </div>

          {/* Right Panel - Details */}
          <div className="flex-1 neumorphic rounded-lg overflow-hidden">
            <DetailPanel selectedNode={selectedNode} />
          </div>
        </div>
      </div>
    </div>
  );
}