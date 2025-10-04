"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Loader2, Sparkles, FileText, Download } from "lucide-react";

interface FRAGOBuilderProps {
  unitId: string;
  unitName: string;
  soldierIds: string[];
  reports: any[];
}

interface FRAGOFields {
  situation: string;
  mission: string;
  execution: string;
  service_support: string;
  command_signal: string;
}

export function FRAGOBuilder({
  unitId,
  unitName,
  soldierIds,
  reports,
}: FRAGOBuilderProps) {
  const [loading, setLoading] = useState(false);
  const [fields, setFields] = useState<FRAGOFields>({
    situation: "",
    mission: "",
    execution: "",
    service_support: "",
    command_signal: "",
  });
  const [generatedDoc, setGeneratedDoc] = useState<string>("");
  const [fragoNumber, setFragoNumber] = useState<number | null>(null);

  // Auto-resize textareas when fields change
  useEffect(() => {
    const textareas = document.querySelectorAll("textarea");
    textareas.forEach((textarea) => {
      textarea.style.height = "auto";
      textarea.style.height = textarea.scrollHeight + "px";
    });
  }, [fields]);

  const handleSuggest = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/frago/suggest", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          unit_id: unitId,
          unit_name: unitName,
          soldier_ids: soldierIds,
          reports: reports,
        }),
      });

      if (!response.ok) throw new Error("Failed to get FRAGO suggestion");

      const data = await response.json();
      setFields(data.suggested_fields);
    } catch (error) {
      console.error("Error getting FRAGO suggestion:", error);
      alert("Failed to get AI suggestion. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleGenerate = async () => {
    setLoading(true);
    try {
      // Get all report IDs
      const reportIds = reports.map((r) => r.report_id).filter(Boolean);

      const response = await fetch("http://localhost:8000/frago/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          unit_id: unitId,
          unit_name: unitName,
          frago_fields: fields,
          source_report_ids: reportIds,
        }),
      });

      if (!response.ok) throw new Error("Failed to generate FRAGO");

      const data = await response.json();
      setGeneratedDoc(data.formatted_document);
      setFragoNumber(data.frago_number);
    } catch (error) {
      console.error("Error generating FRAGO:", error);
      alert("Failed to generate FRAGO. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = () => {
    if (!generatedDoc) return;

    const blob = new Blob([generatedDoc], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `FRAGO_${fragoNumber
      ?.toString()
      .padStart(4, "0")}_${unitName.replace(/\s+/g, "_")}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const updateField = (field: keyof FRAGOFields, value: string) => {
    setFields((prev) => ({ ...prev, [field]: value }));
  };

  return (
    <div className="space-y-2 text-xs h-full overflow-y-auto">
      <Card className="border-0">
        <CardHeader className="p-2">
          <CardTitle className="text-xs font-mono">{unitName}</CardTitle>
          <CardDescription className="text-[10px]">
            {reports.length} reports
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-2 p-2 pt-0">
          <Button
            onClick={handleSuggest}
            disabled={loading || reports.length === 0}
            className="w-full h-6 text-[10px]"
            size="sm"
          >
            {loading ? (
              <Loader2 className="mr-1 h-2 w-2 animate-spin" />
            ) : (
              <Sparkles className="mr-1 h-2 w-2" />
            )}
            AI Suggest
          </Button>

          <div className="space-y-1.5">
            <div>
              <Label htmlFor="situation" className="text-[10px] font-mono">
                1. SIT
              </Label>
              <Textarea
                id="situation"
                value={fields.situation}
                onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => {
                  updateField("situation", e.target.value);
                  e.target.style.height = "auto";
                  e.target.style.height = e.target.scrollHeight + "px";
                }}
                placeholder="Enemy/friendly forces..."
                className="mt-0.5 text-[10px] leading-tight resize-none overflow-hidden"
                rows={2}
              />
            </div>

            <div>
              <Label htmlFor="mission" className="text-[10px] font-mono">
                2. MISSION
              </Label>
              <Textarea
                id="mission"
                value={fields.mission}
                onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => {
                  updateField("mission", e.target.value);
                  e.target.style.height = "auto";
                  e.target.style.height = e.target.scrollHeight + "px";
                }}
                placeholder="Task and purpose..."
                className="mt-0.5 text-[10px] leading-tight resize-none overflow-hidden"
                rows={2}
              />
            </div>

            <div>
              <Label htmlFor="execution" className="text-[10px] font-mono">
                3. EXEC
              </Label>
              <Textarea
                id="execution"
                value={fields.execution}
                onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => {
                  updateField("execution", e.target.value);
                  e.target.style.height = "auto";
                  e.target.style.height = e.target.scrollHeight + "px";
                }}
                placeholder="Concept of operations..."
                className="mt-0.5 text-[10px] leading-tight resize-none overflow-hidden"
                rows={3}
              />
            </div>

            <div>
              <Label
                htmlFor="service_support"
                className="text-[10px] font-mono"
              >
                4. CSS
              </Label>
              <Textarea
                id="service_support"
                value={fields.service_support}
                onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => {
                  updateField("service_support", e.target.value);
                  e.target.style.height = "auto";
                  e.target.style.height = e.target.scrollHeight + "px";
                }}
                placeholder="Logistics..."
                className="mt-0.5 text-[10px] leading-tight resize-none overflow-hidden"
                rows={2}
              />
            </div>

            <div>
              <Label htmlFor="command_signal" className="text-[10px] font-mono">
                5. C2
              </Label>
              <Textarea
                id="command_signal"
                value={fields.command_signal}
                onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => {
                  updateField("command_signal", e.target.value);
                  e.target.style.height = "auto";
                  e.target.style.height = e.target.scrollHeight + "px";
                }}
                placeholder="Command & signal..."
                className="mt-0.5 text-[10px] leading-tight resize-none overflow-hidden"
                rows={2}
              />
            </div>
          </div>

          <div className="flex gap-1.5">
            <Button
              onClick={handleGenerate}
              disabled={loading || !fields.mission}
              className="flex-1 h-6 text-[10px]"
              size="sm"
            >
              {loading ? (
                <Loader2 className="mr-1 h-2 w-2 animate-spin" />
              ) : (
                <FileText className="mr-1 h-2 w-2" />
              )}
              Generate
            </Button>

            {generatedDoc && (
              <Button
                onClick={handleDownload}
                variant="outline"
                size="sm"
                className="h-6 text-[10px]"
              >
                <Download className="mr-1 h-2 w-2" />
                Save
              </Button>
            )}
          </div>
        </CardContent>
      </Card>

      {generatedDoc && (
        <Card className="border-0">
          <CardHeader className="p-2">
            <CardTitle className="text-xs font-mono">
              FRAGO {fragoNumber?.toString().padStart(4, "0")}
            </CardTitle>
          </CardHeader>
          <CardContent className="p-2 pt-0">
            <pre className="whitespace-pre-wrap break-words font-mono text-[9px] bg-muted p-2 rounded-lg leading-[1.3] overflow-x-hidden">
              {generatedDoc}
            </pre>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
