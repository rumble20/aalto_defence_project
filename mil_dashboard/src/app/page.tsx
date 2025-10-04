'use client';

import { useState } from 'react';
import { MilitaryHierarchyTree } from '@/components/military-hierarchy-tree';
import { DetailPanel } from '@/components/detail-panel';
import { StreamPanel } from '@/components/stream-panel';
import { Shield, Users, Activity, FileBarChart, Radio, Layers } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

export default function Home() {
  const [selectedNode, setSelectedNode] = useState<any>(null);
  const [selectedItem, setSelectedItem] = useState<any>(null);
  const [activeTab, setActiveTab] = useState<'hierarchy' | 'reports'>('hierarchy');
  const [selectedUnit, setSelectedUnit] = useState("battalion");

  const handleNodeSelect = (node: any) => {
    setSelectedNode(node);
  };

  const unitLevels = [
    { id: "brigade", name: "Brigade", icon: Layers },
    { id: "battalion", name: "Battalion", icon: Shield },
    { id: "company", name: "Company", icon: Users },
    { id: "platoon", name: "Platoon", icon: Users },
    { id: "squad", name: "Squad", icon: Users },
  ];

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
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 text-sm">
              <Activity className="h-4 w-4 text-foreground" />
              <span className="text-foreground font-mono">LIVE SYSTEM</span>
              <div className="w-2 h-2 bg-foreground rounded-full animate-pulse"></div>
            </div>
          </div>
        </header>

        {/* Tab Navigation */}
        <div className="flex gap-2 bg-card/30 backdrop-blur-sm p-2 rounded-lg neumorphic">
          <Button
            variant={activeTab === 'hierarchy' ? 'default' : 'ghost'}
            onClick={() => setActiveTab('hierarchy')}
            className="font-mono"
          >
            <Shield className="h-4 w-4 mr-2" />
            HIERARCHY
          </Button>
          <Button
            variant={activeTab === 'reports' ? 'default' : 'ghost'}
            onClick={() => setActiveTab('reports')}
            className="font-mono"
          >
            <Radio className="h-4 w-4 mr-2" />
            REPORTS
          </Button>
        </div>

        {/* Main Content */}
        <div className="flex gap-6 h-[calc(100vh-280px)]">
          {activeTab === 'hierarchy' ? (
            <>
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
            </>
          ) : (
            <>
              {/* Left Sidebar - Unit Selector */}
              <div className="w-1/3 neumorphic rounded-lg overflow-hidden p-6">
                <h2 className="text-xl font-bold font-mono text-foreground mb-4 flex items-center gap-2">
                  <Layers className="h-5 w-5" />
                  UNIT LEVELS
                </h2>
                <div className="space-y-2">
                  {unitLevels.map((level) => {
                    const Icon = level.icon;
                    return (
                      <Button
                        key={level.id}
                        variant={selectedUnit === level.id ? 'default' : 'ghost'}
                        onClick={() => setSelectedUnit(level.id)}
                        className="w-full justify-start font-mono"
                      >
                        <Icon className="h-4 w-4 mr-2" />
                        {level.name.toUpperCase()}
                      </Button>
                    );
                  })}
                </div>
              </div>

              {/* Right Panel - Reports Stream */}
              <div className="flex-1 neumorphic rounded-lg overflow-hidden">
                <StreamPanel 
                  streamId={selectedUnit} 
                  onItemClick={setSelectedItem} 
                />
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}