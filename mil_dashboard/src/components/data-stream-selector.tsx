"use client"

import { Button } from "@/components/ui/button"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { ChevronDown, type LucideIcon } from "lucide-react"

interface Stream {
  id: string
  name: string
  icon: LucideIcon
}

interface DataStreamSelectorProps {
  streams: Stream[]
  selectedStream: string
  onStreamChange: (streamId: string) => void
}

export function DataStreamSelector({ streams, selectedStream, onStreamChange }: DataStreamSelectorProps) {
  const currentStream = streams.find((s) => s.id === selectedStream)
  const Icon = currentStream?.icon

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button
          variant="outline"
          className="neumorphic border-0 bg-muted hover:bg-muted/80 transition-all duration-300 shadow-lg"
        >
          {Icon && <Icon className="mr-2 h-4 w-4" />}
          <span className="font-mono">{currentStream?.name}</span>
          <ChevronDown className="ml-2 h-4 w-4 opacity-50" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-56 neumorphic border-border/50 backdrop-blur-xl">
        {streams.map((stream) => {
          const StreamIcon = stream.icon
          return (
            <DropdownMenuItem
              key={stream.id}
              onClick={() => onStreamChange(stream.id)}
              className="cursor-pointer font-mono hover:bg-muted"
            >
              <StreamIcon className="mr-2 h-4 w-4" />
              {stream.name}
            </DropdownMenuItem>
          )
        })}
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
