"use client"

import * as React from "react"
import { cn } from "@/lib/utils"

function Progress({
  className,
  value = 0,
  ...props
}) {
  return (
    <div
      data-slot="progress"
      className={cn(
        "bg-primary/20 relative h-2 w-full overflow-hidden rounded-full",
        className
      )}
      {...props}
    >
      <div
        data-slot="progress-indicator"
        className="bg-primary h-full w-full flex-1 transition-all rounded-full"
        style={{ width: `${Math.min(100, Math.max(0, value || 0))}%` }}
      />
    </div>
  )
}

export { Progress }
