"use client"

import type React from "react"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Loader2 } from "lucide-react"
import { SuggestionCard, type Suggestion } from "@/components/ai/SuggestionCard"

export default function AiAssistantPage() {
  const [userInput, setUserInput] = useState("")
  const [aiResponse, setAiResponse] = useState<{ suggestions: Suggestion[] } | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (!userInput) return
    setIsLoading(true)
    setError(null)
    setAiResponse(null)

    try {
      const res = await fetch("/api/ai-suggestion", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: userInput }),
      })
      const data = await res.json()

      if (data.success) {
        setAiResponse(data.data)
      } else {
        setError(data.error || "Не удалось получить ответ от ИИ.")
      }
    } catch (err: any) {
      setError(err.message || "Ошибка сети.")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <Card className="w-full max-w-2xl mx-auto">
        <CardHeader className="text-center">
          <CardTitle className="text-3xl font-bold">ИИ-помощник по подбору жилья</CardTitle>
          <CardDescription>Введите запрос, и ИИ подберет для вас варианты.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="bg-gray-50 p-4 rounded-lg mb-6">
            <div className="flex items-start space-x-3">
              <Avatar className="w-8 h-8">
                <AvatarFallback className="bg-blue-100 text-blue-600">ИИ</AvatarFallback>
              </Avatar>
              <p className="text-sm text-gray-700">
                Пример: «Двухкомнатная квартира в Краснодаре до 10 млн ₽ рядом с парком».
              </p>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="userInput">Ваш запрос</Label>
              <Input
                id="userInput"
                placeholder="Опишите, что ищете…"
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                required
              />
            </div>
            <Button type="submit" className="w-full" disabled={isLoading}>
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Подбираю…
                </>
              ) : (
                "Начать подбор"
              )}
            </Button>
          </form>
        </CardContent>
      </Card>

      {error && (
        <div className="mt-8 max-w-2xl mx-auto p-4 bg-red-100 text-red-700 rounded-lg">
          <strong>Ошибка:</strong> {error}
        </div>
      )}

      {aiResponse && aiResponse.suggestions && (
        <div className="mt-8">
          <h3 className="text-2xl font-bold mb-6 text-center">Вот что я подобрал для вас:</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {aiResponse.suggestions.map((suggestion, index) => (
              <SuggestionCard key={index} suggestion={suggestion} />
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
