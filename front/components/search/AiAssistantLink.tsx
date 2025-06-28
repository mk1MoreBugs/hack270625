"use client"

import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Bot } from "lucide-react"

export function AiAssistantLink() {
  return (
    <Link href="/ai-assistant" passHref>
      <Button variant="outline" size="sm" className="hidden sm:flex bg-transparent">
        <Bot className="w-4 h-4 mr-2" />
        {"ИИ-подбор"}
      </Button>
    </Link>
  )
}
