"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Send, Radio, AlertTriangle, Shield, Activity, Zap, Eye } from "lucide-react"
import { cn } from "@/lib/utils"

interface StreamPanelProps {
  streamId: string
  onItemClick: (item: any) => void
}

type ReportType = "EOINCREP" | "CASEVAC" | "SITREP" | "MEDEVAC" | "SPOTREP" | "INTREP"

interface BattlefieldReport {
  id: number
  type: ReportType
  text: string
  timestamp: Date
  unit: string
  coordinates?: string
  priority?: "ROUTINE" | "PRIORITY" | "IMMEDIATE" | "FLASH"
  casualties?: number
}

export function StreamPanel({ streamId, onItemClick }: StreamPanelProps) {
  const [message, setMessage] = useState("")
  const [updates, setUpdates] = useState<BattlefieldReport[]>([
    {
      id: 1,
      type: "EOINCREP",
      text: "Enemy patrol spotted, 6 personnel, moving north",
      timestamp: new Date(Date.now() - 120000),
      unit: "Alpha Company",
      coordinates: "38.8977° N, 77.0365° W",
      priority: "PRIORITY",
    },
    {
      id: 2,
      type: "CASEVAC",
      text: "2x casualties, gunshot wounds, requesting immediate evac",
      timestamp: new Date(Date.now() - 180000),
      unit: "Bravo Platoon",
      coordinates: "38.9072° N, 77.0369° W",
      priority: "IMMEDIATE",
      casualties: 2,
    },
    {
      id: 3,
      type: "SITREP",
      text: "Perimeter secure, all checkpoints manned, no contact",
      timestamp: new Date(Date.now() - 240000),
      unit: "Charlie Squad",
      coordinates: "38.8895° N, 77.0353° W",
      priority: "ROUTINE",
    },
    {
      id: 4,
      type: "INTREP",
      text: "Intercepted communications suggest enemy reinforcements inbound",
      timestamp: new Date(Date.now() - 300000),
      unit: "Intel Section",
      coordinates: "38.8920° N, 77.0380° W",
      priority: "PRIORITY",
    },
    {
      id: 5,
      type: "SPOTREP",
      text: "Vehicle movement detected, 3x technical trucks, heading east",
      timestamp: new Date(Date.now() - 360000),
      unit: "Delta Platoon",
      coordinates: "38.8850° N, 77.0340° W",
      priority: "FLASH",
    },
    {
      id: 6,
      type: "MEDEVAC",
      text: "1x heat casualty, stable condition, requesting routine transport",
      timestamp: new Date(Date.now() - 420000),
      unit: "Echo Company",
      coordinates: "38.9000° N, 77.0400° W",
      priority: "ROUTINE",
      casualties: 1,
    },
  ])

  const handleSend = () => {
    if (!message.trim()) return

    const newUpdate: BattlefieldReport = {
      id: updates.length + 1,
      type: "SITREP",
      text: message,
      timestamp: new Date(),
      unit: streamId.charAt(0).toUpperCase() + streamId.slice(1),
      priority: "ROUTINE",
    }

    setUpdates([newUpdate, ...updates])
    setMessage("")
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const getReportTypeColor = (type: ReportType) => {
    return "text-foreground/70"
  }

  const getReportTypeBg = (type: ReportType) => {
    switch (type) {
      case "CASEVAC":
      case "MEDEVAC":
        return "bg-red-500/20 border-red-500/30"
      case "EOINCREP":
      case "SPOTREP":
        return "bg-yellow-500/20 border-yellow-500/30"
      case "INTREP":
        return "bg-blue-500/20 border-blue-500/30"
      case "SITREP":
        return "bg-green-500/20 border-green-500/30"
      default:
        return "bg-foreground/10"
    }
  }

  const getReportIcon = (type: ReportType) => {
    switch (type) {
      case "CASEVAC":
      case "MEDEVAC":
        return AlertTriangle
      case "EOINCREP":
        return Eye
      case "SPOTREP":
        return Zap
      case "INTREP":
        return Activity
      case "SITREP":
        return Shield
      default:
        return Radio
    }
  }

  const getPriorityColor = (priority?: string) => {
    switch (priority) {
      case "FLASH":
      case "IMMEDIATE":
        return "bg-red-500 text-white"
      case "PRIORITY":
        return "bg-yellow-500 text-black"
      default:
        return "bg-foreground/30 text-foreground"
    }
  }

  return (
    <div className="neumorphic border-0 overflow-hidden h-full">
      <div className="p-6 space-y-4 h-full flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold font-mono flex items-center gap-2 text-foreground">
            <Radio className="h-5 w-5" />
            BATTLEFIELD REPORTS
          </h2>
          <div className="flex items-center gap-2">
            <div className="h-2 w-2 rounded-full bg-foreground/50 animate-pulse" />
            <span className="text-xs text-muted-foreground font-mono">LIVE</span>
          </div>
        </div>

        {/* Input Field */}
        <div className="relative">
          <input
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Submit report..."
            className="w-full px-4 py-2 bg-background/50 border border-border rounded-lg pr-12 font-mono text-sm focus:outline-none focus:ring-2 focus:ring-foreground/50"
          />
          <Button
            size="icon"
            onClick={handleSend}
            className="absolute right-1 top-1 h-8 w-8 bg-foreground/10 text-foreground hover:bg-foreground/20 transition-all duration-300"
          >
            <Send className="h-4 w-4" />
          </Button>
        </div>

        {/* Updates Stream */}
        <div className="space-y-2 flex-1 overflow-y-auto pr-2">
          {updates.map((update) => {
            const ReportIcon = getReportIcon(update.type)
            return (
              <div
                key={update.id}
                onClick={() => onItemClick(update)}
                className={cn(
                  "p-4 rounded-lg cursor-pointer transition-all duration-300 hover:scale-[1.02]",
                  "bg-background/50 border border-border",
                  getReportTypeBg(update.type),
                  "hover:shadow-lg",
                )}
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="flex-1 space-y-2">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span
                        className={cn(
                          "px-2 py-0.5 rounded text-xs font-bold font-mono flex items-center gap-1 text-foreground",
                          getReportTypeBg(update.type),
                        )}
                      >
                        <ReportIcon className="h-3 w-3" />
                        {update.type}
                      </span>
                      {update.priority && (
                        <span
                          className={cn(
                            "px-2 py-0.5 rounded text-xs font-bold font-mono",
                            getPriorityColor(update.priority),
                          )}
                        >
                          {update.priority}
                        </span>
                      )}
                      {update.casualties && (
                        <span className="px-2 py-0.5 rounded text-xs font-bold font-mono bg-red-500/30 text-foreground flex items-center gap-1">
                          <AlertTriangle className="h-3 w-3" />
                          {update.casualties}x
                        </span>
                      )}
                    </div>

                    <p className="text-sm font-medium leading-relaxed text-foreground">{update.text}</p>

                    <div className="flex items-center gap-3 text-xs text-muted-foreground font-mono">
                      <span>{update.unit}</span>
                      {update.coordinates && (
                        <>
                          <span>•</span>
                          <span>{update.coordinates}</span>
                        </>
                      )}
                      <span>•</span>
                      <span>{update.timestamp.toLocaleTimeString()}</span>
                    </div>
                  </div>
                  <div className={cn("h-2 w-2 rounded-full mt-2 bg-foreground/50")} />
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}
