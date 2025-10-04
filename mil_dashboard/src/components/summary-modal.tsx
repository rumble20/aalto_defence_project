"use client"

import { useState } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Card } from "@/components/ui/card"
import { FileBarChart, Calendar, Users, TrendingUp, AlertTriangle, Shield } from "lucide-react"

interface SummaryModalProps {
  isOpen: boolean
  onClose: () => void
}

export function SummaryModal({ isOpen, onClose }: SummaryModalProps) {
  const [timeSpan, setTimeSpan] = useState("24h")
  const [unitLevel, setUnitLevel] = useState("battalion")
  const [showSummary, setShowSummary] = useState(false)

  const handleGenerate = () => {
    setShowSummary(true)
  }

  const handleReset = () => {
    setShowSummary(false)
    setTimeSpan("24h")
    setUnitLevel("battalion")
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl bg-card border-border neumorphic">
        <DialogHeader>
          <DialogTitle className="text-2xl font-bold font-mono flex items-center gap-2 text-foreground">
            <FileBarChart className="h-6 w-6" />
            OPERATIONAL SUMMARY
          </DialogTitle>
        </DialogHeader>

        <div className="space-y-6 mt-4">
          {!showSummary ? (
            <>
              {/* Selection Controls */}
              <div className="grid gap-4">
                <div className="space-y-2">
                  <Label htmlFor="timespan" className="text-sm font-mono flex items-center gap-2 text-foreground">
                    <Calendar className="h-4 w-4" />
                    TIME SPAN
                  </Label>
                  <Select value={timeSpan} onValueChange={setTimeSpan}>
                    <SelectTrigger id="timespan" className="neumorphic-inset border-0 font-mono">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="1h">Last 1 Hour</SelectItem>
                      <SelectItem value="6h">Last 6 Hours</SelectItem>
                      <SelectItem value="12h">Last 12 Hours</SelectItem>
                      <SelectItem value="24h">Last 24 Hours</SelectItem>
                      <SelectItem value="48h">Last 48 Hours</SelectItem>
                      <SelectItem value="7d">Last 7 Days</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="unit" className="text-sm font-mono flex items-center gap-2 text-foreground">
                    <Users className="h-4 w-4" />
                    UNIT LEVEL
                  </Label>
                  <Select value={unitLevel} onValueChange={setUnitLevel}>
                    <SelectTrigger id="unit" className="neumorphic-inset border-0 font-mono">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="brigade">Brigade</SelectItem>
                      <SelectItem value="battalion">Battalion</SelectItem>
                      <SelectItem value="company">Company</SelectItem>
                      <SelectItem value="platoon">Platoon</SelectItem>
                      <SelectItem value="squad">Squad</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <Button
                onClick={handleGenerate}
                className="w-full bg-foreground/10 hover:bg-foreground/20 text-foreground font-mono border border-border"
              >
                <TrendingUp className="h-4 w-4 mr-2" />
                GENERATE SUMMARY
              </Button>
            </>
          ) : (
            <>
              <div className="grid gap-4">
                <Card className="p-4 neumorphic-inset border border-border/50">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="p-2 rounded-lg bg-foreground/10">
                        <FileBarChart className="h-5 w-5 text-foreground" />
                      </div>
                      <div>
                        <div className="text-xs text-muted-foreground font-mono">TOTAL REPORTS</div>
                        <div className="text-2xl font-bold font-mono text-foreground">47</div>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-xs text-muted-foreground font-mono">PERIOD</div>
                      <div className="text-sm font-bold font-mono text-foreground">{timeSpan.toUpperCase()}</div>
                    </div>
                  </div>
                </Card>

                <div className="grid grid-cols-2 gap-4">
                  <Card className="p-4 neumorphic-inset border border-military-red/30">
                    <div className="flex items-center gap-3">
                      <div className="p-2 rounded-lg bg-military-red/20">
                        <AlertTriangle className="h-5 w-5 text-foreground" />
                      </div>
                      <div>
                        <div className="text-xs text-muted-foreground font-mono">CASUALTIES</div>
                        <div className="text-2xl font-bold font-mono text-foreground">8</div>
                      </div>
                    </div>
                  </Card>

                  <Card className="p-4 neumorphic-inset border border-military-amber/30">
                    <div className="flex items-center gap-3">
                      <div className="p-2 rounded-lg bg-military-amber/20">
                        <Shield className="h-5 w-5 text-foreground" />
                      </div>
                      <div>
                        <div className="text-xs text-muted-foreground font-mono">ENEMY CONTACTS</div>
                        <div className="text-2xl font-bold font-mono text-foreground">12</div>
                      </div>
                    </div>
                  </Card>
                </div>

                <Card className="p-4 neumorphic-inset border border-border/30">
                  <div className="text-xs text-muted-foreground font-mono mb-3">REPORT BREAKDOWN</div>
                  <div className="space-y-2 font-mono text-sm text-foreground">
                    <div className="flex justify-between">
                      <span>EOINCREP:</span>
                      <span className="font-bold">15</span>
                    </div>
                    <div className="flex justify-between">
                      <span>CASEVAC:</span>
                      <span className="font-bold">5</span>
                    </div>
                    <div className="flex justify-between">
                      <span>SITREP:</span>
                      <span className="font-bold">18</span>
                    </div>
                    <div className="flex justify-between">
                      <span>INTREP:</span>
                      <span className="font-bold">6</span>
                    </div>
                    <div className="flex justify-between">
                      <span>SPOTREP:</span>
                      <span className="font-bold">3</span>
                    </div>
                  </div>
                </Card>

                <Card className="p-4 neumorphic-inset border border-border/30">
                  <div className="text-xs text-muted-foreground font-mono mb-2">UNIT LEVEL</div>
                  <div className="text-lg font-bold font-mono capitalize text-foreground">{unitLevel}</div>
                </Card>
              </div>

              <div className="flex gap-3">
                <Button onClick={handleReset} variant="outline" className="flex-1 font-mono bg-transparent">
                  NEW SUMMARY
                </Button>
                <Button
                  onClick={onClose}
                  className="flex-1 bg-foreground/10 hover:bg-foreground/20 text-foreground font-mono border border-border"
                >
                  CLOSE
                </Button>
              </div>
            </>
          )}
        </div>
      </DialogContent>
    </Dialog>
  )
}
