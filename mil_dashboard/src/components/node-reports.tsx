"use client";

import { Card } from "@/components/ui/card";
import {
  FileText,
  AlertTriangle,
  Shield,
  Activity,
  Eye,
  Zap,
} from "lucide-react";
import { cn } from "@/lib/utils";
import type { TreeNode } from "./hierarchy-tree";

interface Report {
  report_id: string;
  soldier_id: string;
  soldier_name: string;
  unit_id: string;
  unit_name: string;
  timestamp: string;
  report_type: string;
  structured_json: string | object;
  confidence: number;
}

interface NodeReportsProps {
  selectedNode: TreeNode | null;
  reports: Report[];
  loading: boolean;
  onReportClick?: (report: Report) => void;
}

export function NodeReports({
  selectedNode,
  reports,
  loading,
  onReportClick,
}: NodeReportsProps) {
  const getReportIcon = (type: string) => {
    switch (type) {
      case "CASEVAC":
      case "MEDEVAC":
        return AlertTriangle;
      case "EOINCREP":
        return Eye;
      case "SPOTREP":
        return Zap;
      case "INTREP":
      case "INTELLIGENCE":
        return Activity;
      case "SITREP":
        return Shield;
      case "CONTACT":
        return AlertTriangle;
      case "LOGSTAT":
        return FileText;
      default:
        return FileText;
    }
  };

  const getReportColor = (type: string) => {
    switch (type) {
      case "CASEVAC":
      case "MEDEVAC":
        return "bg-military-red/20 border-military-red/30 text-military-red";
      case "EOINCREP":
      case "SPOTREP":
      case "CONTACT":
        return "bg-military-amber/20 border-military-amber/30 text-military-amber";
      case "INTREP":
      case "INTELLIGENCE":
        return "bg-military-blue/20 border-military-blue/30 text-military-blue";
      case "SITREP":
      case "LOGSTAT":
        return "bg-military-olive/20 border-military-olive/30 text-military-olive";
      default:
        return "bg-muted/20 border-border/30 text-foreground";
    }
  };

  const getReportSummary = (report: Report) => {
    try {
      const data =
        typeof report.structured_json === "string"
          ? JSON.parse(report.structured_json)
          : report.structured_json;

      if (data.status) return data.status;
      if (data.observation) return data.observation;
      if (data.description) return data.description;
      if (data.engagement_status) return data.engagement_status;

      return JSON.stringify(data).substring(0, 100);
    } catch {
      return "No summary available";
    }
  };

  if (!selectedNode) {
    return (
      <Card className="neumorphic border-0 h-full flex items-center justify-center">
        <div className="text-center text-muted-foreground">
          <FileText className="h-12 w-12 mx-auto mb-4 opacity-50" />
          <p className="font-mono">Select a node to view reports</p>
        </div>
      </Card>
    );
  }

  return (
    <Card className="neumorphic border-0 h-full flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-border/50">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-bold font-mono text-foreground">
              REPORTS
            </h3>
            <p className="text-xs text-muted-foreground font-mono mt-1">
              {selectedNode.name}{" "}
              {selectedNode.type === "unit" && "& subordinates"}
            </p>
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold font-mono text-foreground">
              {reports.length}
            </div>
            <div className="text-xs text-muted-foreground font-mono">Total</div>
          </div>
        </div>
      </div>

      {/* Reports List */}
      <div className="flex-1 overflow-y-auto p-2 space-y-1">
        {loading ? (
          <div className="flex items-center justify-center py-12 text-muted-foreground">
            Loading reports...
          </div>
        ) : reports.length === 0 ? (
          <div className="flex items-center justify-center py-12 text-muted-foreground text-sm">
            No reports available for this {selectedNode.type}
          </div>
        ) : (
          reports.map((report) => {
            const Icon = getReportIcon(report.report_type);
            const colorClass = getReportColor(report.report_type);

            return (
              <div
                key={report.report_id}
                onClick={() => onReportClick?.(report)}
                className={cn(
                  "p-2 rounded-lg border cursor-pointer transition-all duration-200",
                  "hover:scale-[1.01] neumorphic-inset",
                  colorClass
                )}
              >
                <div className="flex items-start gap-3">
                  <div className="flex-shrink-0 mt-0.5">
                    <Icon className="h-3 w-3" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-0.5">
                      <span className="text-[10px] font-bold font-mono">
                        {report.report_type}
                      </span>
                      <span className="text-[10px] text-muted-foreground font-mono">
                        {new Date(report.timestamp).toLocaleString()}
                      </span>
                    </div>
                    <p className="text-xs text-foreground line-clamp-2 mb-0.5 leading-tight">
                      {getReportSummary(report)}
                    </p>
                    <div className="flex items-center gap-2 text-[10px] text-muted-foreground font-mono">
                      <span>{report.soldier_name || "Unknown"}</span>
                      {report.unit_name && (
                        <>
                          <span>•</span>
                          <span>{report.unit_name}</span>
                        </>
                      )}
                      <span>•</span>
                      <span>{(report.confidence * 100).toFixed(0)}% conf.</span>
                    </div>
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>

      {/* Summary Stats */}
      {reports.length > 0 && (
        <div className="p-2 border-t border-border/50">
          <div className="grid grid-cols-3 gap-1 text-center">
            {Array.from(new Set(reports.map((r) => r.report_type)))
              .slice(0, 3)
              .map((type) => {
                const count = reports.filter(
                  (r) => r.report_type === type
                ).length;
                return (
                  <div key={type} className="neumorphic-inset rounded-lg p-1">
                    <div className="text-sm font-bold font-mono text-foreground">
                      {count}
                    </div>
                    <div className="text-[10px] text-muted-foreground font-mono">
                      {type}
                    </div>
                  </div>
                );
              })}
          </div>
        </div>
      )}
    </Card>
  );
}
