"use client";

import { cn } from "@/lib/utils";
import type React from "react";
import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import {
  ChevronDown,
  ChevronUp,
  X,
  MapPin,
  FileText,
  Activity,
  AlertTriangle,
} from "lucide-react";
import {
  Line,
  LineChart,
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart";

interface ReportDrawerProps {
  selectedItem: any;
  onClose: () => void;
}

const chartData = [
  { time: "00:00", incidents: 2 },
  { time: "04:00", incidents: 1 },
  { time: "08:00", incidents: 4 },
  { time: "12:00", incidents: 3 },
  { time: "16:00", incidents: 5 },
  { time: "20:00", incidents: 2 },
];

export function ReportDrawer({ selectedItem, onClose }: ReportDrawerProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [expandedSections, setExpandedSections] = useState({
    location: true,
    timeline: true,
    metadata: false,
  });

  useEffect(() => {
    setIsOpen(!!selectedItem);
  }, [selectedItem]);

  const toggleSection = (section: keyof typeof expandedSections) => {
    setExpandedSections((prev) => ({
      ...prev,
      [section]: !prev[section],
    }));
  };

  const handleClose = () => {
    setIsOpen(false);
    setTimeout(onClose, 300);
  };

  if (!selectedItem) return null;

  // Parse structured JSON if it's a string
  const structuredData =
    typeof selectedItem.structured_json === "string"
      ? JSON.parse(selectedItem.structured_json)
      : selectedItem.structured_json || {};

  return (
    <>
      {/* Backdrop */}
      <div
        className={cn(
          "fixed inset-0 bg-black/60 backdrop-blur-sm transition-opacity duration-300 z-40",
          isOpen ? "opacity-100" : "opacity-0 pointer-events-none"
        )}
        onClick={handleClose}
      />

      {/* Drawer */}
      <div
        className={cn(
          "fixed right-0 top-0 h-full w-full md:w-[500px] bg-card border-l border-border neumorphic z-50",
          "transition-transform duration-300 ease-in-out overflow-y-auto",
          isOpen ? "translate-x-0" : "translate-x-full"
        )}
      >
        <div className="p-6 space-y-4">
          {/* Header */}
          <div className="flex items-start justify-between sticky top-0 bg-card/95 backdrop-blur-sm pb-4 border-b border-border">
            <div className="space-y-1">
              <h2 className="text-xl font-bold font-mono text-foreground">
                REPORT DETAILS
              </h2>
              <p className="text-sm text-muted-foreground">
                {selectedItem.report_type || "UNKNOWN"} -{" "}
                {selectedItem.soldier_name || "Unknown"}
              </p>
            </div>
            <Button
              size="icon"
              variant="ghost"
              onClick={handleClose}
              className="hover:bg-foreground/10 text-foreground"
            >
              <X className="h-4 w-4" />
            </Button>
          </div>

          {/* Content */}
          <div className="space-y-3">
            <CollapsibleSection
              title="Report Information"
              icon={MapPin}
              isExpanded={expandedSections.location}
              onToggle={() => toggleSection("location")}
            >
              <div className="space-y-3">
                <div className="p-4 rounded-lg bg-muted/30 font-mono">
                  <div className="text-xs text-muted-foreground mb-1">
                    TIMESTAMP
                  </div>
                  <div className="text-lg font-bold text-foreground">
                    {new Date(selectedItem.timestamp).toLocaleString()}
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div className="p-3 rounded-lg bg-muted/30">
                    <div className="text-xs text-muted-foreground font-mono mb-1">
                      UNIT
                    </div>
                    <div className="text-sm font-bold font-mono text-foreground">
                      {selectedItem.unit_name || "Unknown"}
                    </div>
                  </div>
                  <div className="p-3 rounded-lg bg-muted/30">
                    <div className="text-xs text-muted-foreground font-mono mb-1">
                      CONFIDENCE
                    </div>
                    <div className="text-sm font-bold font-mono text-foreground">
                      {((selectedItem.confidence || 0) * 100).toFixed(0)}%
                    </div>
                  </div>
                </div>

                {/* Display structured data fields */}
                {Object.keys(structuredData).length > 0 && (
                  <div className="p-4 rounded-lg bg-foreground/10 border border-foreground/20">
                    <div className="text-xs text-muted-foreground font-mono mb-2">
                      REPORT DATA
                    </div>
                    <div className="space-y-2">
                      {Object.entries(structuredData).map(([key, value]) => (
                        <div key={key} className="flex justify-between">
                          <span className="text-xs font-mono text-muted-foreground">
                            {key}:
                          </span>
                          <span className="text-xs font-mono text-foreground font-bold">
                            {typeof value === "object"
                              ? JSON.stringify(value)
                              : String(value)}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </CollapsibleSection>

            <CollapsibleSection
              title="Incident Timeline"
              icon={Activity}
              isExpanded={expandedSections.timeline}
              onToggle={() => toggleSection("timeline")}
            >
              <ChartContainer
                config={{
                  incidents: {
                    label: "Incidents",
                    color: "hsl(var(--foreground))",
                  },
                }}
                className="h-[200px] w-full"
              >
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={chartData}>
                    <CartesianGrid
                      strokeDasharray="3 3"
                      stroke="oklch(0.2 0 0)"
                    />
                    <XAxis
                      dataKey="time"
                      stroke="oklch(0.65 0 0)"
                      fontSize={10}
                      fontFamily="var(--font-mono)"
                    />
                    <YAxis
                      stroke="oklch(0.65 0 0)"
                      fontSize={10}
                      fontFamily="var(--font-mono)"
                    />
                    <ChartTooltip content={<ChartTooltipContent />} />
                    <Line
                      type="monotone"
                      dataKey="incidents"
                      stroke="var(--color-incidents)"
                      strokeWidth={2}
                      dot={{ fill: "var(--color-incidents)", r: 4 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </ChartContainer>
            </CollapsibleSection>

            <CollapsibleSection
              title="Report Metadata"
              icon={FileText}
              isExpanded={expandedSections.metadata}
              onToggle={() => toggleSection("metadata")}
            >
              <div className="space-y-2 font-mono text-xs">
                <div className="p-2 rounded bg-muted/30">
                  <span className="text-muted-foreground">Report ID: </span>
                  <span className="text-foreground">
                    {selectedItem.report_id}
                  </span>
                </div>
                <div className="p-2 rounded bg-muted/30">
                  <span className="text-muted-foreground">Soldier ID: </span>
                  <span className="text-foreground">
                    {selectedItem.soldier_id}
                  </span>
                </div>
                <div className="p-2 rounded bg-muted/30">
                  <span className="text-muted-foreground">Unit ID: </span>
                  <span className="text-foreground">
                    {selectedItem.unit_id}
                  </span>
                </div>
                <div className="p-2 rounded bg-muted/30">
                  <span className="text-muted-foreground">Report Type: </span>
                  <span className="text-foreground">
                    {selectedItem.report_type}
                  </span>
                </div>
              </div>
            </CollapsibleSection>
          </div>
        </div>
      </div>
    </>
  );
}

function CollapsibleSection({
  title,
  icon: Icon,
  isExpanded,
  onToggle,
  children,
}: {
  title: string;
  icon: any;
  isExpanded: boolean;
  onToggle: () => void;
  children: React.ReactNode;
}) {
  return (
    <div className="neumorphic-inset rounded-lg overflow-hidden border border-border/30">
      <button
        onClick={onToggle}
        className="w-full p-4 flex items-center justify-between hover:bg-muted/50 transition-colors"
      >
        <div className="flex items-center gap-2">
          <Icon className="h-4 w-4 text-foreground/70" />
          <span className="font-semibold text-sm font-mono text-foreground">
            {title}
          </span>
        </div>
        {isExpanded ? (
          <ChevronUp className="h-4 w-4 text-muted-foreground" />
        ) : (
          <ChevronDown className="h-4 w-4 text-muted-foreground" />
        )}
      </button>
      {isExpanded && <div className="p-4 pt-0">{children}</div>}
    </div>
  );
}

function LogEntry({
  time,
  message,
  status,
}: {
  time: string;
  message: string;
  status?: string;
}) {
  return (
    <div className="flex items-start gap-2 p-2 rounded bg-muted/30">
      <span className="text-muted-foreground min-w-[60px]">{time}</span>
      <span
        className={cn(
          "leading-relaxed",
          status === "priority"
            ? "text-foreground font-bold"
            : "text-foreground/80"
        )}
      >
        {message}
      </span>
    </div>
  );
}
