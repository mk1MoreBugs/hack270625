import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Tag, Home, Layers, Calendar, Eye } from "lucide-react"
import Link from "next/link"
import Image from "next/image"

// Определяем тип для одного предложения, чтобы использовать его в других компонентах
export interface Suggestion {
  id?: number
  address: string
  description: string
  price: number
  area: number
  rooms: number
  floor: number
  total_floors: number
  year_built: number
  image?: string // Добавляем поле для изображения
}

interface SuggestionCardProps {
  suggestion: Suggestion
}

export function SuggestionCard({ suggestion }: SuggestionCardProps) {
  const formatPrice = (price: number) => {
    return new Intl.NumberFormat("ru-RU", {
      style: "currency",
      currency: "RUB",
      maximumFractionDigits: 0,
    }).format(price)
  }

  // Генерируем ID квартиры для ссылки (используем индекс или ID если есть)
  const apartmentId = suggestion.id ? `1-a${suggestion.id}` : "1-a1"

  return (
    <Card className="flex flex-col overflow-hidden">
      {/* Изображение ЖК */}
      {suggestion.image && (
        <div className="relative h-48 w-full">
          <Image src={suggestion.image || "/placeholder.svg"} alt={suggestion.address} fill className="object-cover" />
        </div>
      )}

      <CardHeader>
        <CardTitle>{suggestion.address}</CardTitle>
        <CardDescription>{suggestion.description}</CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col flex-grow">
        <div className="mb-4 text-2xl font-bold text-blue-600">{formatPrice(suggestion.price)}</div>
        <div className="grid grid-cols-2 gap-4 text-sm text-gray-700 mb-4">
          <div className="flex items-center gap-2">
            <Home className="h-4 w-4 text-gray-500" />
            <span>{suggestion.rooms} комн.</span>
          </div>
          <div className="flex items-center gap-2">
            <Tag className="h-4 w-4 text-gray-500" />
            <span>{suggestion.area} м²</span>
          </div>
          <div className="flex items-center gap-2">
            <Layers className="h-4 w-4 text-gray-500" />
            <span>
              {suggestion.floor}/{suggestion.total_floors} этаж
            </span>
          </div>
          <div className="flex items-center gap-2">
            <Calendar className="h-4 w-4 text-gray-500" />
            <span>{suggestion.year_built} г.</span>
          </div>
        </div>
        <div className="mt-auto space-y-2">
          <Link href={`/project/${apartmentId}`}>
            <Button className="w-full">Посмотреть детали</Button>
          </Link>
          <Link
            href="https://connector.eagle3dstreaming.com/v5/zvnd/Kubinka/default"
            target="_blank"
            rel="noopener noreferrer"
          >
            <Button variant="outline" className="w-full bg-transparent">
              <Eye className="w-4 h-4 mr-2" />
              3D-Тур ЖК
            </Button>
          </Link>
        </div>
      </CardContent>
    </Card>
  )
}
