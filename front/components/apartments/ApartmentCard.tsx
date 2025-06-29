import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { MapPin, Star, Home } from "lucide-react"
import Image from "next/image"
import Link from "next/link"
import type { Apartment } from "@/lib/types"

interface ApartmentCardProps {
  apartment: Apartment
}

export function ApartmentCard({ apartment }: ApartmentCardProps) {
  const getRoomsText = (rooms: number | undefined) => {
    if (rooms === undefined || rooms === null) return "Студия"
    if (rooms === 0) return "Студия"
    return `${rooms}-комн`
  }

  return (
    <Card className="overflow-hidden hover:shadow-xl transition-shadow">
      <div className="relative">
        <Image
          src={apartment.image || "/placeholder.svg"}
          alt={apartment.name}
          width={400}
          height={300}
          className="w-full h-48 object-cover"
        />
        <Badge className="absolute top-4 left-4 bg-red-500 hover:bg-red-600">{apartment.promotion}</Badge>
        <Badge variant="secondary" className="absolute top-4 right-4">
          {getRoomsText(apartment.rooms)}
        </Badge>
      </div>

      <CardHeader>
        <div className="flex items-start justify-between">
          <div>
            <CardTitle className="text-lg mb-1">{apartment.name}</CardTitle>
            <CardDescription className="flex items-center">
              <MapPin className="w-4 h-4 mr-1" />
              {apartment.project}
            </CardDescription>
          </div>
          <div className="flex items-center">
            <Star className="w-4 h-4 text-yellow-400 fill-current mr-1" />
            <span className="text-sm font-medium">4.8</span>
          </div>
        </div>
      </CardHeader>

      <CardContent>
        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Площадь:</span>
            <span className="font-medium">{apartment.area} м²</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Этаж:</span>
            <span className="font-medium">{apartment.floor || 5}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Комнат:</span>
            <span className="font-medium flex items-center">
              <Home className="w-4 h-4 mr-1" />
              {getRoomsText(apartment.rooms)}
            </span>
          </div>
          <div className="pt-3 border-t">
            <div className="flex justify-between items-center mb-4">
              <span className="text-2xl font-bold text-blue-600">{apartment.price}</span>
            </div>
            <div className="flex space-x-2">
              <Link href={`/project/${apartment.id}`} className="flex-1">
                <Button className="w-full">Подробнее</Button>
              </Link>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
