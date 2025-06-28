import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"

export default function AiAssistantPage() {
  return (
    <div className="container mx-auto px-4 py-8 flex justify-center">
      <div className="max-w-md w-full space-y-6">
        <div className="text-center">
          <h1 className="text-3xl font-bold">ИИ-помощник по подбору жилья</h1>
          <p className="text-gray-500">Расскажите о ваших предпочтениях, и я подберу идеальные варианты</p>
        </div>
        <div className="space-y-4 rounded-lg border bg-card text-card-foreground shadow-sm p-6">
          <div className="bg-gray-50 p-4 rounded-lg">
            <div className="flex items-start space-x-3">
              <Avatar className="w-8 h-8">
                <AvatarFallback className="bg-blue-100 text-blue-600">ИИ</AvatarFallback>
              </Avatar>
              <div className="flex-1">
                <p className="text-sm text-gray-700">
                  Привет! Я помогу найти идеальную квартиру. Какой у вас бюджет и в каком районе ищете?
                </p>
              </div>
            </div>
          </div>
          <Input placeholder="Напишите ваш запрос..." />
          <Button className="w-full">Начать подбор</Button>
        </div>
      </div>
    </div>
  )
}
