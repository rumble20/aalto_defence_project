"use client";

import { useState } from "react";
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
    <div className="space-y-2 text-xs">
      <Card className="border-0">
        <CardHeader className="p-3">
          <CardTitle className="text-sm font-mono">{unitName}</CardTitle>
          <CardDescription className="text-xs">
            {reports.length} reports
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-2 p-3 pt-0">
          <Button
            onClick={handleSuggest}
            disabled={loading || reports.length === 0}
            className="w-full h-7 text-xs"
            size="sm"
          >
            {loading ? (
              <Loader2 className="mr-1 h-3 w-3 animate-spin" />
            ) : (
              <Sparkles className="mr-1 h-3 w-3" />
            )}
            AI Suggest
          </Button>

          <div className="space-y-2">
            <div>
              <Label htmlFor="situation" className="text-xs font-mono">
                1. SIT
              </Label>
              <Textarea
                id="situation"
                value={fields.situation}
                onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) =>
                  updateField("situation", e.target.value)
                }
                placeholder="Enemy/friendly forces..."
                className="min-h-[50px] mt-1 text-xs"
              />
            </div>

            <div>
              <Label htmlFor="mission" className="text-xs font-mono">
                2. MISSION
              </Label>
              <Textarea
                id="mission"
                value={fields.mission}
                onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) =>
                  updateField("mission", e.target.value)
                }
                placeholder="Task and purpose..."
                className="min-h-[50px] mt-1 text-xs"
              />
            </div>

            <div>
              <Label htmlFor="execution" className="text-xs font-mono">
                3. EXEC
              </Label>
              <Textarea
                id="execution"
                value={fields.execution}
                onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) =>
                  updateField("execution", e.target.value)
                }
                placeholder="Concept of operations..."
                className="min-h-[60px] mt-1 text-xs"
              />
            </div>

            <div>
              <Label htmlFor="service_support" className="text-xs font-mono">
                4. CSS
              </Label>
              <Textarea
                id="service_support"
                value={fields.service_support}
                onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) =>
                  updateField("service_support", e.target.value)
                }
                placeholder="Logistics..."
                className="min-h-[50px] mt-1 text-xs"
              />
            </div>

            <div>
              <Label htmlFor="command_signal" className="text-xs font-mono">
                5. C2
              </Label>
              <Textarea
                id="command_signal"
                value={fields.command_signal}
                onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) =>
                  updateField("command_signal", e.target.value)
                }
                placeholder="Command & signal..."
                className="min-h-[50px] mt-1 text-xs"
              />
            </div>
          </div>

          <div className="flex gap-2">
            <Button
              onClick={handleGenerate}
              disabled={loading || !fields.mission}
              className="flex-1 h-7 text-xs"
              size="sm"
            >
              {loading ? (
                <Loader2 className="mr-1 h-3 w-3 animate-spin" />
              ) : (
                <FileText className="mr-1 h-3 w-3" />
              )}
              Generate
            </Button>

            {generatedDoc && (
              <Button
                onClick={handleDownload}
                variant="outline"
                size="sm"
                className="h-7 text-xs"
              >
                <Download className="mr-1 h-3 w-3" />
                Save
              </Button>
            )}
          </div>
        </CardContent>
      </Card>

      {generatedDoc && (
        <Card className="border-0">
          <CardHeader className="p-3">
            <CardTitle className="text-sm font-mono">
              FRAGO {fragoNumber?.toString().padStart(4, "0")}
            </CardTitle>
          </CardHeader>
          <CardContent className="p-3 pt-0">
            <pre className="whitespace-pre-wrap font-mono text-[10px] bg-muted p-2 rounded-lg leading-tight max-h-[300px] overflow-y-auto">
              {generatedDoc}
            </pre>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
